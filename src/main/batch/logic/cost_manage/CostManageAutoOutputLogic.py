# coding: UTF-8
'''
経費データ自動出力バッチ処理ロジック

@author: takanori_gozu
'''
from copy import copy
from src.main.batch.base.BaseLogic import BaseLogic
from src.main.batch.base.Config import Config
from src.main.batch.dao.EmployeeDao import EmployeeDao
from src.main.batch.dao.ExpensesDao import ExpensesDao
from src.main.batch.lib.date.DateUtilLib import DateUtilLib
from src.main.batch.lib.excel.PythonExcelLib import PythonExcelLib
from src.main.batch.lib.file.FileOperationLib import FileOperationLib
from src.main.batch.lib.mail.SendMailLib import SendMailLib
from src.main.batch.lib.string.StringOperationLib import StringOperationLib

class CostManageAutoOutputLogic(BaseLogic):

    roundTripTypeMap = {'1':'片道', '2':'往復', '3':'定期'}

    '''
    コンストラクタ
    '''
    def __init__(self, db, logger, form):
        super(CostManageAutoOutputLogic, self).__init__(db, logger, form)

    def run(self):

        self.writeLog('処理開始')

        date = self.getForm('-date')

        if date == '':
            self.writeLog('parameter:-date is not set')
            return

        #前回データを削除
        self.deleteLastSessionData()

        #処理する社員情報を取得
        employeeList = self.getEmployeeList()
        dt = DateUtilLib.toDateTimeDate(date)
        dt = StringOperationLib.toString(DateUtilLib.getDateIntervalMonth(dt, -1))

        targetYm = StringOperationLib.mid(dt, 1, dt.rfind('-'))

        #ループ内
        for i in range(len(employeeList)):

            userId = StringOperationLib.toString(employeeList[i][EmployeeDao.COL_ID])
            name = StringOperationLib.toString(employeeList[i][EmployeeDao.COL_NAME])
            loginId = StringOperationLib.toString(employeeList[i][EmployeeDao.COL_LOGIN_ID])

            self.writeLog('処理対象社員名 : ' + name)

            #個人ディレクトリを作成
            employeeDir = self.makeEmployeeDir(name)

            #データを取得
            trafficList = self.getExpensesList(userId, targetYm, '1')
            expensesList = self.getExpensesList(userId, targetYm, '2')

            #1件でもあれば、精算書を作成
            if len(trafficList) > 0:
                self.makeTrafficExcel(targetYm, trafficList, name, employeeDir)
            if len(expensesList) > 0:
                self.makeExpensesExcel(targetYm, expensesList, name, employeeDir)

            #領収書ファイルがあれば、コピー
            self.copyReceiptFile(targetYm, loginId, employeeDir)

        #Zipにまとめる
        self.makeZipFile()

        #メール送信
        self.sendCostManage(targetYm)

        self.writeLog('処理完了')

        return

    '''
    前回処理データを削除する
    '''
    def deleteLastSessionData(self):
        #全て消してから新たに作成する
        dirPath = Config.getConf('CostManageAutoDLinfo', 'download_path')
        FileOperationLib.deleteDir(dirPath)
        FileOperationLib.makeDir(dirPath)

        #Zipファイル
        FileOperationLib.deleteFile(Config.getConf('CostManageAutoDLinfo', 'output_path') + 'cost_manage.zip')

    '''
    社員情報を取得する
    '''
    def getEmployeeList(self):
        dao = EmployeeDao(self.db)

        dao.addSelect(EmployeeDao.COL_ID)
        dao.addSelect(EmployeeDao.COL_NAME)
        dao.addSelect(EmployeeDao.COL_LOGIN_ID)

        dao.addWhereStr(EmployeeDao.COL_RETIREMENT, '0') #退職者は除く
        dao.addWhereStr(EmployeeDao.COL_USER_LEVEL, '2', EmployeeDao.COMP_GREATER_EQUAL) #管理権限は除く

        dao.addOrder(EmployeeDao.COL_HIRAGANA) #50音順で処理

        return dao.doSelect()

    '''
    Zip格納用の個人ディレクトリを作成する
    '''
    def makeEmployeeDir(self, employeeName):
        dirPath = Config.getConf('CostManageAutoDLinfo', 'download_path') + employeeName + '/'
        FileOperationLib.makeDir(dirPath)

        return dirPath

    '''
    精算データを取得
    '''
    def getExpensesList(self, userId, registYm, inputType):
        dao = ExpensesDao(self.db)

        dao.addSelect(ExpensesDao.COL_EXPENSES_YMD)
        if inputType == '1':
            #交通費の場合
            dao.addSelect(ExpensesDao.COL_ROUND_TRIP_TYPE)
            dao.addSelect(ExpensesDao.COL_TRANSPORT)
            dao.addSelect(ExpensesDao.COL_FROM_PLACE)
            dao.addSelect(ExpensesDao.COL_TO_PLACE)

        elif inputType == '2':
            #経費の場合
            dao.addSelect(ExpensesDao.COL_PAY_TYPE)
            dao.addSelect(ExpensesDao.COL_EXPENSES_TYPE)

        dao.addSelect(ExpensesDao.COL_EXPENSES_DETAIL)
        dao.addSelect(ExpensesDao.COL_COST)

        dao.addWhere(ExpensesDao.COL_EMPLOYEE_ID, userId)
        dao.addWhereStr(ExpensesDao.COL_INPUT_TYPE, inputType)
        dao.addWhereStr(ExpensesDao.COL_REGIST_YM, registYm)

        select = dao.doSelect()

        expensesList = []

        for i in range(len(select)):
            expensesYmd = StringOperationLib.toString(select[i][ExpensesDao.COL_EXPENSES_YMD])
            expensesYmd = DateUtilLib.getDateFormatJapanese(expensesYmd)
            if inputType == '1':
                roundTrip = ''
                #交通費
                if select[i][ExpensesDao.COL_ROUND_TRIP_TYPE] != None:
                    roundTrip = self.roundTripTypeMap[select[i][ExpensesDao.COL_ROUND_TRIP_TYPE]]
                expensesList.append([expensesYmd, roundTrip, select[i][ExpensesDao.COL_TRANSPORT], select[i][ExpensesDao.COL_FROM_PLACE], select[i][ExpensesDao.COL_TO_PLACE], select[i][ExpensesDao.COL_EXPENSES_DETAIL], select[i][ExpensesDao.COL_COST]])
            elif inputType == '2':
                #経費(現金、立替金は固定出力)
                expensesList.append([expensesYmd, '現金', '立替金', select[i][ExpensesDao.COL_EXPENSES_DETAIL], select[i][ExpensesDao.COL_COST]])

        return expensesList

    '''
    交通費精算書の作成
    '''
    def makeTrafficExcel(self, targetYm, trafficList, employeeName, path):

        trafficName = '交通費精算書'

        year, month = DateUtilLib.splitYm(targetYm)
        lastDay = DateUtilLib.getLastDay(StringOperationLib.toInt(year), StringOperationLib.toInt(month))
        ym = DateUtilLib.getYmFormatJapanese(targetYm)
        ymd = ym + StringOperationLib.toString(lastDay) + '日'
        name = StringOperationLib.replace(employeeName, " ", "")

        excel = PythonExcelLib()
        excel.setPageA4
        excel.setOrientation()

        excel.rename(trafficName)

        #タイトル等共通部分
        self.setCommon(excel, ym, ymd, name, trafficName)

        #項目名
        self.setTrafficTitle(excel)

        #データ
        lastRow = self.setListValue(excel, trafficList)

        #合計
        self.setCostSumValue(excel, copy(lastRow), 'G')

        #体裁
        self.trafficExcelFormat(excel, copy(lastRow))

        excel.save(path + trafficName + '.xlsx')

        #オブジェクト解放
        del excel

    '''
    経費精算書の作成
    '''
    def makeExpensesExcel(self, targetYm, expensesList, employeeName, path):

        expensesName = '経費精算書'

        year, month = DateUtilLib.splitYm(targetYm)
        lastDay = DateUtilLib.getLastDay(StringOperationLib.toInt(year), StringOperationLib.toInt(month))
        ym = DateUtilLib.getYmFormatJapanese(targetYm)
        ymd = ym + StringOperationLib.toString(lastDay) + '日'
        name = StringOperationLib.replace(employeeName, " ", "")

        excel = PythonExcelLib()
        excel.setPageA4
        excel.setOrientation()

        excel.rename(expensesName)

        #タイトル等共通部分
        self.setCommon(excel, ym, ymd, name, expensesName)

        #項目名
        self.setExpensesTitle(excel)

        #データ
        lastRow = self.setListValue(excel, expensesList)

        #合計
        self.setCostSumValue(excel, lastRow, 'E')

        #体裁
        self.expensesExcelFormat(excel, copy(lastRow))

        excel.save(path + expensesName + '.xlsx')

        #オブジェクト解放
        del excel

    '''
    共通部分
    '''
    def setCommon(self, excel, ym, ymd, name, fileName):

        excel.setValueA1('A1', fileName)
        excel.setValueA1('A2', '氏名')
        excel.setValueA1('A3', '精算月')
        excel.setValueA1('A4', '提出日')
        excel.setValueA1('B2', name)
        excel.setValueA1('B3', ym)
        excel.setValueA1('B4', ymd)

        #フォント
        excel.changeSize('A1', 18)

        excel.changeFontMulti('A1:H500', 'Meiryo UI')

        #余白
        excel.setMargin(0.5, 0.5, 0.8, 0, 0.5, 0.5)

    '''
    交通費精算書の項目名
    '''
    def setTrafficTitle(self, excel):

        row = 6

        excel.setValueR1C1(1, row, '日付')
        excel.setValueR1C1(2, row, '往復路')
        excel.setValueR1C1(3, row, '手段')
        excel.setValueR1C1(4, row, '出発')
        excel.setValueR1C1(5, row, '到着')
        excel.setValueR1C1(6, row, '目的')
        excel.setValueR1C1(7, row, '金額')
        excel.setValueR1C1(8, row, '領収書')

        excel.setValueR1C1(7, 2, '交通費合計')

    '''
    経費精算書の項目名
    '''
    def setExpensesTitle(self, excel):

        row = 6

        excel.setValueR1C1(1, row, '日付')
        excel.setValueR1C1(2, row, '支払方法')
        excel.setValueR1C1(3, row, '内訳')
        excel.setValueR1C1(4, row, '内容')
        excel.setValueR1C1(5, row, '金額')
        excel.setValueR1C1(6, row, '領収書')

        excel.setValueR1C1(5, 2, '経費合計')

    '''
    データ部分
    '''
    def setListValue(self, excel, targetList):

        row = 7

        for i in range(len(targetList)):
            col = 1
            for j in range(len(targetList[i])):
                excel.setValueR1C1(col, row, targetList[i][j])
                col += 1
            row += 1

        if row < 30:
            row = 30

        return row

    '''
    金額の合計
    '''
    def setCostSumValue(self, excel, lastRow, col):

        totalRow = lastRow + 1

        excel.setValueA1(col + StringOperationLib.toString(totalRow), '=SUM(' + col + '7:' + col + StringOperationLib.toString(lastRow) + ')')
        excel.setValueA1(col + '3', '=' + col  + StringOperationLib.toString(totalRow))

    '''
    体裁の調整(交通費精算書)
    '''
    def trafficExcelFormat(self, excel, lastRow):

        #列幅
        excel.setCellWidth('A', 15)
        excel.setCellWidth('B', 12)
        excel.setCellWidth('C', 12)
        excel.setCellWidth('D', 15)
        excel.setCellWidth('E', 15)
        excel.setCellWidth('F', 35)
        excel.setCellWidth('G', 15)
        excel.setCellWidth('H', 7)

        #結合
        excel.mergeCell('A1:H1')
        excel.mergeCell('B2:C2')
        excel.mergeCell('B3:C3')
        excel.mergeCell('B4:C4')
        excel.mergeCell('G2:H2')
        excel.mergeCell('G3:H4')

        #フォントサイズ
        excel.changeSizeMulti('A7:H' + StringOperationLib.toString(lastRow), 9)
        excel.changeSize('G3', 18)

        #背景色
        excel.changeCellBackColorMulti('A2:A4', 'DBDBDB')
        excel.changeCellBackColorMulti('A6:H6', 'DBDBDB')
        excel.changeCellBackColorMulti('G2:H2', 'DBDBDB')

        #罫線
        excel.setBorderMulti('A6:H' + StringOperationLib.toString(lastRow + 1), 'hair')
        excel.setBorderMulti('A6:H6', 'thin', '000000', 'top')
        excel.setBorderMulti('H6:H' + StringOperationLib.toString(lastRow + 1), 'thin', '000000', 'right')
        excel.setBorderMulti('A' + StringOperationLib.toString(lastRow + 1) + ':H' + StringOperationLib.toString(lastRow + 1), 'thin', '000000', 'top')
        excel.setBorderMulti('A' + StringOperationLib.toString(lastRow + 1) + ':H' + StringOperationLib.toString(lastRow + 1), 'thin', '000000', 'bottom')
        excel.setBorderMulti('A6:A' + StringOperationLib.toString(lastRow + 1), 'thin', '000000', 'left')

        excel.setBorderMulti('A2:C4')
        excel.setBorderMulti('G2:H4')

        #位置
        excel.setAlignment('A1', 'top', 'center')
        excel.setAlignment('G2', 'top', 'center')
        excel.setAlignment('G3', 'center', 'center')
        excel.setAlignmentMulti('A6:H6', 'center', 'center')
        excel.setAlignmentMulti('F7:F' + StringOperationLib.toString(lastRow), 'center', 'left', True)

        #フォーマット
        excel.setNumberFormat('G3', '#,##0')

    '''
    体裁の調整(経費精算書)
    '''
    def expensesExcelFormat(self, excel, lastRow):

        #列幅
        excel.setCellWidth('A', 15)
        excel.setCellWidth('B', 15)
        excel.setCellWidth('C', 15)
        excel.setCellWidth('D', 40)
        excel.setCellWidth('E', 15)
        excel.setCellWidth('F', 7)

        #結合
        excel.mergeCell('A1:F1')
        excel.mergeCell('B2:C2')
        excel.mergeCell('B3:C3')
        excel.mergeCell('B4:C4')
        excel.mergeCell('E2:F2')
        excel.mergeCell('E3:F4')

        #フォントサイズ
        excel.changeSizeMulti('A7:H' + StringOperationLib.toString(lastRow), 9)
        excel.changeSize('E3', 18)

        #背景色
        excel.changeCellBackColorMulti('A2:A4', 'DBDBDB')
        excel.changeCellBackColorMulti('A6:F6', 'DBDBDB')
        excel.changeCellBackColorMulti('E2:F2', 'DBDBDB')

        #罫線
        excel.setBorderMulti('A6:F' + StringOperationLib.toString(lastRow + 1), 'hair')
        excel.setBorderMulti('A6:F6', 'thin', '000000', 'top')
        excel.setBorderMulti('F6:F' + StringOperationLib.toString(lastRow + 1), 'thin', '000000', 'right')
        excel.setBorderMulti('A' + StringOperationLib.toString(lastRow + 1) + ':F' + StringOperationLib.toString(lastRow + 1), 'thin', '000000', 'top')
        excel.setBorderMulti('A' + StringOperationLib.toString(lastRow + 1) + ':F' + StringOperationLib.toString(lastRow + 1), 'thin', '000000', 'bottom')
        excel.setBorderMulti('A6:A' + StringOperationLib.toString(lastRow + 1), 'thin', '000000', 'left')

        excel.setBorderMulti('A2:C4')
        excel.setBorderMulti('E2:F4')

        #位置
        excel.setAlignment('A1', 'top', 'center')
        excel.setAlignment('E2', 'top', 'center')
        excel.setAlignment('E3', 'center', 'center')
        excel.setAlignmentMulti('A6:F6', 'center', 'center')
        excel.setAlignmentMulti('D7:D' + StringOperationLib.toString(lastRow), 'center', 'left', True)

        #フォーマット
        excel.setNumberFormat('E3', '#,##0')

    '''
    領収書ファイルをコピーする
    '''
    def copyReceiptFile(self, targetYm, loginId, toPath):

        year, month = DateUtilLib.splitYm(targetYm)

        ym = StringOperationLib.toString(year) + StringOperationLib.toString(month)

        fromPath = FileOperationLib.getFileList(Config.getConf('RECEIPTinfo', 'receipt_file_path') + loginId + '/' + ym + '/')

        for file in fromPath:
            if not(StringOperationLib.match(FileOperationLib.getFileName(file), '*.xlsx')):
                fileName = FileOperationLib.getFileName(file).encode('utf-8', 'surrogateescape').decode('SJIS', 'surrogateescape')
                FileOperationLib.copyFile(file, toPath +  fileName)

    '''
    送付用のZipファイルを作成する
    '''
    def makeZipFile(self):

        dirPath = Config.getConf('CostManageAutoDLinfo', 'download_path')
        outputPath = Config.getConf('CostManageAutoDLinfo', 'output_path')

        FileOperationLib.fileArchive('cost_manage', outputPath, dirPath)

    '''
    メール送信
    '''
    def sendCostManage(self, dt):

        ym = DateUtilLib.getYmFormatJapanese(dt)

        mail = SendMailLib()

        mail.setMailFrom(Config.getConf('MAILinfo', 'admin_mail_from'))
        mail.setMailTo(Config.getConf('CostManageAutoDLinfo', 'kanri_mail'))
        mail.setMailSubject('【自動送信】' + ym + '経費精算情報')
        mail.setMailText(ym + '分の経費精算一覧を送付します。')
        mail.setAttach(Config.getConf('CostManageAutoDLinfo', 'output_path') + 'cost_manage.zip')

        mail.send()