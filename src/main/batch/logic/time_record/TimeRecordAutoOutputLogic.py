# coding: UTF-8
'''
勤怠自動出力バッチ処理ロジック

@author: takanori_gozu
'''
import glob
import calendar
import zipfile
import os
from datetime import datetime
from copy import copy
from dateutil.relativedelta import relativedelta
from src.main.batch.base.BaseLogic import BaseLogic
from src.main.batch.base.Config import Config
from src.main.batch.lib.mail.SendMail import SendMail
from src.main.batch.lib.string.StringOperation import StringOperation
from src.main.batch.dao.EmployeeDao import EmployeeDao
from src.main.batch.dao.HolidayDao import HolidayDao
from src.main.batch.dao.TimeRecordDao import TimeRecordDao
from src.main.batch.lib.excel.PythonExcel import PythonExcel
from src.main.batch.lib.collection.Collection import Collection
from _decimal import Decimal

class TimeRecordAutoOutputLogic(BaseLogic):

    weekdayList = ['月', '火', '水', '木', '金', '土', '日', '祝']
    classMap = {'1':'出勤', '2':'休日出勤', '3':'有休', '4':'振休', '5':'欠勤', '6':'公休', '7':'年末年始休暇', '8':'夏季休暇'}

    '''
    コンストラクタ
    '''
    def __init__(self, db, logger, form):
        super(TimeRecordAutoOutputLogic, self).__init__(db, logger, form)

    '''
    run
    '''
    def run(self):

        self.writeLog('処理開始')

        date = self.getForm('-date')

        if date == '':
            self.writeLog('parameter:-date is not set')
            return

        #前回処理分を削除
        self.deleteLastSessionData()

        #処理する社員情報を取得
        employeeMap = self.getEmployeeMap()
        dt = StringOperation.toString((datetime.strptime(date + ' 00:00:00', '%Y-%m-%d %H:%M:%S') - relativedelta(months=1)).date())

        #祝祭日マスタを取得しておく
        holidayList = self.getHolidayList(dt, date)

        #ループ
        for id, name in employeeMap.items():

            self.writeLog('処理対象社員名 : ' + name)

            #勤怠データを取得
            timeRecordMaplist = self.getTimeRecordMapList(id, dt, date, holidayList)
            totalList = self.getTotalList(id, dt, date)
            #Excel作成
            self.makeExcel(dt, timeRecordMaplist, totalList, name)

        #作成したExcelをZipにまとめる
        self.makeZipFile()

        #メールで送信する
        self.sendTimeSheet(dt)

        self.writeLog('処理完了')

        return

    '''
    前回処理分を削除する
    '''
    def deleteLastSessionData(self):
        files = glob.glob(Config.getConf('TimeRecordAutoDLinfo', 'download_path') + '*')
        for file in files:
            os.remove(file)

    '''
    処理する社員情報を取得する
    '''
    def getEmployeeMap(self):

        dao = EmployeeDao(self.db)

        dao.addSelect(EmployeeDao.COL_ID)
        dao.addSelect(EmployeeDao.COL_NAME)
        dao.addWhereStr(EmployeeDao.COL_RETIREMENT, '0') #退職者は除く
        dao.addWhereStr(EmployeeDao.COL_USER_LEVEL, '2', EmployeeDao.COMP_GREATER_EQUAL) #管理者は除く

        dao.addOrder(EmployeeDao.COL_HIRAGANA) #50音順で処理

        return Collection.toMap(dao.doSelect())

    '''
    祝祭日マスタを取得
    '''
    def getHolidayList(self, fromDt, toDt):

        dao = HolidayDao(self.db)

        dao.addSelect(HolidayDao.COL_HOLIDAY_DATE)
        dao.addWhereStr(HolidayDao.COL_HOLIDAY_DATE, fromDt, HolidayDao.COMP_GREATER_EQUAL)
        dao.addWhereStr(HolidayDao.COL_HOLIDAY_DATE, toDt, HolidayDao.COMP_LESS)

        select = dao.doSelectCol(HolidayDao.COL_HOLIDAY_DATE)
        list = []

        for i in range(len(select)):
            list.append(select[i].strftime('%Y-%m-%d'))

        return list

    '''
    処理対象の勤怠データを取得
    '''
    def getTimeRecordMapList(self, employeeId, fromDt, toDt, holidayList):

        #Base
        baseMap = self.makeBaseMap(fromDt, holidayList)

        #DB
        dbMap = self.getDbMap(employeeId, fromDt, toDt)

        #マージ
        self.mergeMap(baseMap, dbMap)

        return baseMap

    '''
    空のListを生成
    '''
    def makeBaseMap(self, dt, holidayList):

        y = int(dt.split('-')[0])
        m = int(dt.split('-')[1])

        baseMap = {}

        _, lastday = calendar.monthrange(y,m)
        hi = datetime.strptime(dt + ' 00:00:00', '%Y-%m-%d %H:%M:%S')

        for x in range(lastday):

            weekday = hi.weekday()
            day = int(StringOperation.toString(hi.date()).split('-')[2]);

            if StringOperation.toString(hi.date()) in holidayList:
                weekday = 7

            baseMap[StringOperation.toString(hi.date())] = [day, self.weekdayList[weekday], '', '', '', '', '', '', '', '', '', '', '']
            hi = hi + relativedelta(days=1)

        return baseMap

    '''
    DBの値を取得してMapを生成
    '''
    def getDbMap(self, employeeId, fromDt, toDt):

        dbMap = {}

        dao = TimeRecordDao(self.db)

        dao.addSelect(TimeRecordDao.COL_WORK_DATE)
        dao.addSelect(TimeRecordDao.COL_CLASSIFICATION)
        dao.addSelect(TimeRecordDao.COL_START_TIME)
        dao.addSelect(TimeRecordDao.COL_END_TIME)
        dao.addSelect(TimeRecordDao.COL_BREAK_TIME)
        dao.addSelect(TimeRecordDao.COL_PRESCRIBED_TIME)
        dao.addSelect(TimeRecordDao.COL_OVER_WORK_TIME)
        dao.addSelect(TimeRecordDao.COL_MIDNIGHT_TIME)
        dao.addSelect(TimeRecordDao.COL_MIDNIGHT_BREAK_TIME)
        dao.addSelect(TimeRecordDao.COL_MIDNIGHT_OVER_WORK_TIME)
        dao.addSelect(TimeRecordDao.COL_WORK_TIME)
        dao.addSelect(TimeRecordDao.COL_REMARK)

        dao.addWhere(TimeRecordDao.COL_EMPLOYEE_ID, str(employeeId))
        dao.addWhereStr(TimeRecordDao.COL_WORK_DATE, fromDt, TimeRecordDao.COMP_GREATER_EQUAL)
        dao.addWhereStr(TimeRecordDao.COL_WORK_DATE, toDt, TimeRecordDao.COMP_LESS)
        dao.addWhereIn(TimeRecordDao.COL_SCENE, [1,3]) #共通と本社用のみ取得してくる

        select = dao.doSelect()

        for i in range(len(select)):
            key = StringOperation.toString(select[i][TimeRecordDao.COL_WORK_DATE])
            clsVal = self.classMap[select[i][TimeRecordDao.COL_CLASSIFICATION]]
            startTime = self.intToHM(select[i][TimeRecordDao.COL_START_TIME])
            endTime = self.intToHM(select[i][TimeRecordDao.COL_END_TIME])
            breakTime = self.intToHM(select[i][TimeRecordDao.COL_BREAK_TIME])
            prescribedTime = self.intToHM(select[i][TimeRecordDao.COL_PRESCRIBED_TIME])
            overWorkTime = self.intToHM(select[i][TimeRecordDao.COL_OVER_WORK_TIME])
            midnightTime = self.intToHM(select[i][TimeRecordDao.COL_MIDNIGHT_TIME])
            midnightBreakTime = self.intToHM(select[i][TimeRecordDao.COL_MIDNIGHT_BREAK_TIME])
            midnightOverWorkTime = self.intToHM(select[i][TimeRecordDao.COL_MIDNIGHT_OVER_WORK_TIME])
            workTime = self.intToHM(select[i][TimeRecordDao.COL_WORK_TIME])
            remark = select[i][TimeRecordDao.COL_REMARK]
            dbMap[key] = [clsVal, startTime, endTime, breakTime, prescribedTime, overWorkTime, midnightTime, midnightBreakTime, midnightOverWorkTime, workTime, remark]

        return dbMap

    '''
    時間のフォーマット変換(Int→hh:mm)
    '''
    def intToHM(self, timeInt):

        if timeInt == None: return None
        h, m = divmod(timeInt, 60)

        return StringOperation.toString(h) + ':' + StringOperation.toString(m).zfill(2)

    '''
    時間のフォーマット変換(Int→0.00h)
    '''
    def intToHMM(self, timeInt):

        if timeInt == None: return None
        h, m = divmod(timeInt, 60)

        if m >= 0 and m < 15:
            m = Decimal(0)
        elif m >= 15 and m < 30:
            m = Decimal(0.25)
        elif m >= 30 and m < 45:
            m = Decimal(0.5)
        else:
            m = Decimal(0.75)

        return '{:.2f}'.format(h + m) + 'h'

    '''
    BaseにDB値をマージする
    '''
    def mergeMap(self, baseMap, dbMap):
        for k, v in baseMap.items():
            if k in dbMap:
                idx = 2 #base側の開始
                dv = dbMap[k]
                for mv in dv:
                    v[idx] = mv
                    idx += 1

    '''
    合計値を取得する
    '''
    def getTotalList(self, employeeId, fromDt, toDt):

        dao = TimeRecordDao(self.db)

        dao.addSelectSumAs(TimeRecordDao.COL_BREAK_TIME, 'total_break_time')
        dao.addSelectSumAs(TimeRecordDao.COL_PRESCRIBED_TIME, 'total_prescribed_time')
        dao.addSelectSumAs(TimeRecordDao.COL_OVER_WORK_TIME, 'total_over_work_time')
        dao.addSelectSumAs(TimeRecordDao.COL_MIDNIGHT_TIME, 'total_midnight_time')
        dao.addSelectSumAs(TimeRecordDao.COL_MIDNIGHT_BREAK_TIME, 'total_midnight_break_time')
        dao.addSelectSumAs(TimeRecordDao.COL_MIDNIGHT_OVER_WORK_TIME, 'total_midnight_over_work_time')
        dao.addSelectSumAs(TimeRecordDao.COL_WORK_TIME, 'total_work_time')

        dao.addWhere(TimeRecordDao.COL_EMPLOYEE_ID, StringOperation.toString(employeeId))
        dao.addWhereStr(TimeRecordDao.COL_WORK_DATE, fromDt, TimeRecordDao.COMP_GREATER_EQUAL)
        dao.addWhereStr(TimeRecordDao.COL_WORK_DATE, toDt, TimeRecordDao.COMP_LESS)
        dao.addWhereIn(TimeRecordDao.COL_SCENE, [1,3]) #共通と本社用のみ取得してくる

        return dao.doSelectInfo()

    '''
    勤怠表の作成
    '''
    def makeExcel(self, dt, recordMapList, totalList, name):

        y = int(dt.split('-')[0])
        m = int(dt.split('-')[1])

        ym = StringOperation.toString(y) + '年' + StringOperation.toString(m) + '月'
        name = StringOperation.replace(name, " ", "")

        excel = PythonExcel()
        excel.setPageA4

        excel.rename('月間作業実績報告書')

        #タイトル等共通部分
        self.setCommon(excel, ym, name)

        #勤怠表の項目名
        self.setTimeRecordTitle(excel)

        #勤怠表
        lastRow = self.setTimeRecordValue(excel, recordMapList)

        #合計行
        self.setTimeRecordTotalValue(excel, totalList, copy(lastRow))

        #押印欄等
        self.setOtherArea(excel, copy(lastRow))

        #体裁
        self.setFormat(excel, copy(lastRow))

        excel.save(Config.getConf('TimeRecordAutoDLinfo', 'download_path') + '本社提出用_' + ym + '勤怠表_' + name + '.xlsx')

        #オブジェクト解放
        del excel

    '''
    共通部分
    '''
    def setCommon(self, excel, ym, name):

        excel.setValueA1('A1', '月間作業実績報告書')
        excel.setValueA1('K3', '所属')
        excel.setValueA1('A4', ym)
        excel.setValueA1('K4', '氏名')
        excel.setValueA1('L4', name)

    '''
    勤怠表のタイトル部分
    '''
    def setTimeRecordTitle(self, excel):

        row = 5

        excel.setValueR1C1(1, row, '日付')
        excel.setValueR1C1(2, row, '曜日')
        excel.setValueR1C1(3, row, '区分')
        excel.setValueR1C1(4, row, '出勤')
        excel.setValueR1C1(5, row, '退勤')
        excel.setValueR1C1(6, row, '休憩')
        excel.setValueR1C1(7, row, '所定')
        excel.setValueR1C1(8, row, '残業')
        excel.setValueR1C1(9, row, '深夜')
        excel.setValueR1C1(10, row, '深夜休憩')
        excel.setValueR1C1(11, row, '深夜残業')
        excel.setValueR1C1(12, row, '労働')
        excel.setValueR1C1(13, row, '備考')

    '''
    勤怠表の値部分
    '''
    def setTimeRecordValue(self, excel, listMap):

        row = 6

        for key, vals in listMap.items():
            col = 1
            for value in vals:
                if value != None:
                    excel.setValueR1C1(col, row, value)
                col += 1
            row += 1

        return row

    '''
    勤怠表の合計部分
    '''
    def setTimeRecordTotalValue(self, excel, totalList, lastRow):

        row = lastRow
        col = 1

        excel.setValueR1C1(col, row, '合計')
        col+=5
        for value in totalList.values():
            if value != None and value != 0:
                excel.setValueR1C1(col, row, self.intToHM(value))
            col+=1

        row+=1
        col = 1
        excel.setValueR1C1(col, row, '総時間')
        col+=5
        for value in totalList.values():
            if value != None and value != 0:
                excel.setValueR1C1(col, row, self.intToHMM(value))
            col+=1

    '''
    その他
    '''
    def setOtherArea(self, excel, lastRow):

        row = lastRow + 3

        #実出勤日数、就業時間数
        excel.setValueR1C1(10, row, '実出勤日数')
        excel.setValueR1C1(12, row, '=COUNTA(E6:E' + StringOperation.toString(lastRow) + ') & "日"')
        row+=1
        excel.setValueR1C1(10, row, '就業時間数')
        excel.setValueR1C1(12, row, '=L' + StringOperation.toString(lastRow + 1))

        #連絡欄
        row+=2
        excel.setValueR1C1(1, row, '連絡欄')

        #押印欄
        row+=6
        excel.setValueR1C1(9, row, '確認')
        excel.setValueR1C1(11, row, '承認')

    '''
    体裁の調整
    '''
    def setFormat(self, excel, lastRow):

        excel.setMargin(0.5, 0.5, 0, 0, 0.5, 0.5)

        #列幅
        excel.setCellWidth('A', 5)
        excel.setCellWidth('B', 5)
        excel.setCellWidth('C', 15)
        excel.setCellWidth('D', 6)
        excel.setCellWidth('E', 6)
        excel.setCellWidth('F', 7)
        excel.setCellWidth('G', 8)
        excel.setCellWidth('H', 7)
        excel.setCellWidth('I', 7)
        excel.setCellWidth('J', 7)
        excel.setCellWidth('K', 7)
        excel.setCellWidth('L', 8)
        excel.setCellWidth('M', 20)

        #行高
        excel.setRowHeight(5, 30)
        for i in range(6, lastRow + 2):
            excel.setRowHeight(i, 15)

        #着色
        excel.changeCellBackColorMulti('A5:M5', 'FFFF00')
        excel.changeCellBackColorMulti('D6:E' + StringOperation.toString(lastRow - 1), '00FFFF')
        excel.changeCellBackColorMulti('G6:L' + StringOperation.toString(lastRow - 1), '00FFFF')

        #結合
        excel.mergeCell('A1:M1') #タイトル
        excel.mergeCell('A4:C4') #年月
        excel.mergeCell('L4:M4') #氏名
        excel.mergeCell('A' + StringOperation.toString(lastRow) + ':E' + StringOperation.toString(lastRow)) #合計
        excel.mergeCell('A' + StringOperation.toString(lastRow + 1) + ':E' + StringOperation.toString(lastRow + 1)) #総時間
        excel.mergeCell('J' + StringOperation.toString(lastRow + 3) + ':K' + StringOperation.toString(lastRow + 3)) #実出勤日数
        excel.mergeCell('L' + StringOperation.toString(lastRow + 3) + ':M' + StringOperation.toString(lastRow + 3))
        excel.mergeCell('J' + StringOperation.toString(lastRow + 4) + ':K' + StringOperation.toString(lastRow + 4)) #就業時間数
        excel.mergeCell('L' + StringOperation.toString(lastRow + 4) + ':M' + StringOperation.toString(lastRow + 4))
        excel.mergeCell('A' + StringOperation.toString(lastRow + 6) + ':M' + StringOperation.toString(lastRow + 6)) #連絡欄
        excel.mergeCell('A' + StringOperation.toString(lastRow + 7) + ':M' + StringOperation.toString(lastRow + 10))
        excel.mergeCell('I' + StringOperation.toString(lastRow + 12) + ':J' + StringOperation.toString(lastRow + 12)) #確認欄
        excel.mergeCell('I' + StringOperation.toString(lastRow + 13) + ':J' + StringOperation.toString(lastRow + 16))
        excel.mergeCell('K' + StringOperation.toString(lastRow + 12) + ':L' + StringOperation.toString(lastRow + 12)) #承認欄
        excel.mergeCell('K' + StringOperation.toString(lastRow + 13) + ':L' + StringOperation.toString(lastRow + 16))

        #文字位置等
        excel.setAlignment('A1', 'top', 'center')
        excel.setAlignment('A4', 'top', 'center')
        excel.setAlignment('L4', 'top', 'center')
        excel.setAlignmentMulti('A5:M5', 'center', 'center', True)
        excel.setAlignmentMulti('A6:L' + StringOperation.toString(lastRow + 1), 'center', 'center')
        excel.setAlignmentMulti('M6:M'+ StringOperation.toString(lastRow - 1), 'top', 'left', True)
        excel.setAlignment('I'+ StringOperation.toString(lastRow + 12), 'top', 'center')
        excel.setAlignment('K'+ StringOperation.toString(lastRow + 12), 'top', 'center')

        #罫線
        excel.setBorderMulti('A5:M'+ StringOperation.toString(lastRow + 1))
        excel.setBorderMulti('J' + StringOperation.toString(lastRow + 3) + ':M'+ StringOperation.toString(lastRow + 4))
        excel.setBorderMulti('A'  + StringOperation.toString(lastRow + 6) + ':M'+ StringOperation.toString(lastRow + 10))
        excel.setBorderMulti('I' + StringOperation.toString(lastRow + 12) + ':L'+ StringOperation.toString(lastRow + 16))

        #1ページに収める
        excel.setFitToPage()

    '''
    送付用のZipファイルを作成する
    '''
    def makeZipFile(self):

        filePath = glob.glob(Config.getConf('TimeRecordAutoDLinfo', 'download_path') + '*')

        with zipfile.ZipFile(Config.getConf('TimeRecordAutoDLinfo', 'download_path') + 'time_sheet.zip', 'w', compression=zipfile.ZIP_DEFLATED) as newZip:
            for file in filePath:
                newZip.write(file, arcname=os.path.basename(file))

    '''
    メール送信
    '''
    def sendTimeSheet(self, dt):

        y = int(dt.split('-')[0])
        m = int(dt.split('-')[1])

        ym = StringOperation.toString(y) + '年' + StringOperation.toString(m) + '月'

        mail = SendMail()

        mail.setMailFrom(Config.getConf('MAILinfo', 'admin_mail_from'))
        mail.setMailTo(Config.getConf('TimeRecordAutoDLinfo', 'kanri_mail'))
        mail.setMailSubject('【自動送信】' + ym + '勤怠表')
        mail.setMailText(ym + '分の勤怠表を送付します。')
        mail.setAttach(Config.getConf('TimeRecordAutoDLinfo', 'download_path') + 'time_sheet.zip')

        mail.send()