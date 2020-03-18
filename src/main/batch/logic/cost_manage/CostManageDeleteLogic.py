# coding: UTF-8
'''
経費データ削除バッチ処理ロジック

@author: takanori_gozu
'''
from src.main.batch.base.BaseLogic import BaseLogic
from src.main.batch.base.Config import Config
from src.main.batch.dao.ExpensesDao import ExpensesDao
from src.main.batch.dao.EmployeeDao import EmployeeDao
from src.main.batch.lib.date.DateUtilLib import DateUtilLib
from src.main.batch.lib.collection.CollectionLib import CollectionLib
from src.main.batch.lib.string.StringOperationLib import StringOperationLib
from src.main.batch.lib.file.FileOperationLib import FileOperationLib

class CostManageDeleteLogic(BaseLogic):

    '''
    コンストラクタ
    '''
    def __init__(self, db, logger, form):
        super(CostManageDeleteLogic, self).__init__(db, logger, form)

    '''
    run
    '''
    def run(self):
        date = self.getForm('-date')

        if date == '':
            self.writeLog('parameter:-date is not set')
            return

        #削除対象の基準を取得
        stdDate = self.getStandardDate(date)

        #削除基準の日付List
        targetList = self.getDeleteTarget(stdDate)

        #データを削除する
        count = self.deleteData(stdDate)

        if count > 0:
            #領収書ファイルを削除する
            self.deleteReceiptFile(targetList)

        return

    '''
    データ削除の基準日を取得する
    '''
    def getStandardDate(self, dt):
        date = DateUtilLib.toDateTimeDate(dt)
        #文字列で返す
        return StringOperationLib.toString(DateUtilLib.getDateIntervalYear(date, -3))

    '''
    削除対象年月リストの取得
    '''
    def getDeleteTarget(self, dt):
        dao = ExpensesDao(self.db)

        dao.addSelectAs(ExpensesDao.COL_REGIST_YM, 'ym')
        dao.addWhereStr(ExpensesDao.COL_REGIST_YM, dt, ExpensesDao.COMP_LESS)
        dao.addGroupBy('ym')

        return CollectionLib.toStringList(dao.doSelect(), 'ym')

    '''
    経費データの削除
    '''
    def deleteData(self, dt):
        self.writeLog('削除基準日:' + dt)

        dao = ExpensesDao(self.db)

        dao.addWhereStr(ExpensesDao.COL_REGIST_YM, dt, ExpensesDao.COMP_LESS)

        count = dao.doCount()

        self.writeLog('削除対象データ件数:' + StringOperationLib.toString(count) + '件')

        dao.doDelete()

        return count

    '''
    領収書ファイルの削除
    '''
    def deleteReceiptFile(self, arr):
        #社員情報を取得
        eDao = EmployeeDao(self.db)
        eDao.addWhereStr(EmployeeDao.COL_LOGIN_ID, Config.getConf('DBinfo', 'admin_user_id'), EmployeeDao.COMP_NOT_EQUAL) #管理者は除外

        eList = eDao.doSelectCol(EmployeeDao.COL_LOGIN_ID)

        self.writeLog('ディレクトリ削除開始:' + StringOperationLib.toString(DateUtilLib.getToday()))

        for i in range(len(eList)):
            for j in range(len(arr)):
                ym = StringOperationLib.toString(StringOperationLib.left(arr[j], 4) + StringOperationLib.right(arr[j], 2))
                user_id = StringOperationLib.toString(eList[i])
                dirPath = Config.getConf('RECEIPTinfo', 'receipt_file_path') + user_id + '/' + ym
                if FileOperationLib.existDir(dirPath):
                    FileOperationLib.deleteDir(dirPath)
                    self.writeLog('ディレクトリ削除 ユーザーID: ' + user_id + ' 対象年月: ' + ym)

        self.writeLog('ディレクトリ削除完了:' + StringOperationLib.toString(DateUtilLib.getToday()))