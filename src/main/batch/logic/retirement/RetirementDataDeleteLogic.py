# coding: UTF-8
'''
退職者データ削除バッチ処理ロジック

@author: takanori_gozu
'''
import os.path
import shutil
from datetime import datetime
from dateutil.relativedelta import relativedelta
from src.main.batch.base.BaseLogic import BaseLogic
from src.main.batch.base.Config import Config
from src.main.batch.dao.EmployeeDao import EmployeeDao
from src.main.batch.lib.string.StringOperation import StringOperation
from src.main.batch.dao.WeeklyReportDao import WeeklyReportDao
from src.main.batch.dao.TimeRecordDao import TimeRecordDao
from src.main.batch.dao.ExpensesDao import ExpensesDao
from src.main.batch.dao.TimeRecordConfigDao import TimeRecordConfigDao

class RetirementDataDeleteLogic(BaseLogic):

    '''
    コンストラクタ
    '''
    def __init__(self, db, logger, form):
        super(RetirementDataDeleteLogic, self).__init__(db, logger, form)

    '''
    run
    '''
    def run(self):
        date = self.getForm('-date')

        if date == '':
            self.writeLog('parameter:-date is not set')
            return

        #基準日を取得(3年保持)
        stdDate = self.getStandardDate(date)

        self.writeLog('削除基準日：' + stdDate)

        #退職後3年以上経過した社員のIDを取得
        ids = self.getDeleteTargetIds(stdDate)

        if len(ids) == 0:
            self.writeLog('退職者データなし')
            return

        #週報データを削除
        self.deleteWeeklyReportData(ids)
        #勤怠データを削除
        self.deleteTimeRecordData(ids)
        #勤怠設定データを削除
        self.deleteTimeRecordConfigData(ids)
        #経費データを削除
        self.deleteExpensesData(ids)
        #社員データを削除
        self.deleteEmployeeData(ids)

        return

    '''
    削除基準日を取得する(3年保持)
    '''
    def getStandardDate(self, dt):
        date = dt + ' 00:00:00'
        bdt = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

        #文字列で返す
        return StringOperation.toString((bdt - relativedelta(years=3)).date())

    '''
    削除対象の社員IDを取得
    '''
    def getDeleteTargetIds(self, dt):
        dao = EmployeeDao(self.db)

        dao.addWhereStr(EmployeeDao.COL_RETIREMENT, '1')
        dao.addWhereStr(EmployeeDao.COL_RETIREMENT_DATE, dt, EmployeeDao.COMP_LESS)

        return dao.doSelectCol(EmployeeDao.COL_ID)

    '''
    週報データを削除する
    '''
    def deleteWeeklyReportData(self, ids):
        dao = WeeklyReportDao(self.db)

        dao.addWhereIn(WeeklyReportDao.COL_REGIST_USER_ID, ids)

        count = dao.doCount()

        self.writeLog('週報データ削除対象件数：' + StringOperation.toString(count) + '件')
        dao.doDelete()

        return

    '''
    勤怠データを削除する
    '''
    def deleteTimeRecordData(self, ids):
        dao = TimeRecordDao(self.db)

        dao.addWhereIn(TimeRecordDao.COL_EMPLOYEE_ID, ids)

        count = dao.doCount()

        self.writeLog('勤怠データ削除対象件数：' + StringOperation.toString(count) + '件')
        dao.doDelete()

        return

    '''
    勤怠設定データを削除する
    '''
    def deleteTimeRecordConfigData(self, ids):
        dao = TimeRecordConfigDao(self.db)

        dao.addWhereIn(TimeRecordConfigDao.COL_EMPLOYEE_ID, ids)

        count = dao.doCount()

        self.writeLog('勤怠設定データ削除対象件数：' + StringOperation.toString(count) + '件')
        dao.doDelete()

        return

    '''
    経費データを削除する
    '''
    def deleteExpensesData(self, ids):
        dao = ExpensesDao(self.db)

        dao.addWhereIn(ExpensesDao.COL_EMPLOYEE_ID, ids)

        count = dao.doCount()

        self.writeLog('勤怠データ削除対象件数：' + StringOperation.toString(count) + '件')
        dao.doDelete()

        #領収書ファイル
        self.deleteReceiptFile(ids)

        return

    '''
    領収書ファイル格納のディレクトリを削除する
    '''
    def deleteReceiptFile(self, ids):
        #社員情報を取得
        eDao = EmployeeDao(self.db)
        eDao.addWhereIn(EmployeeDao.COL_ID, ids)

        eList = eDao.doSelectCol(EmployeeDao.COL_LOGIN_ID)

        self.writeLog('ディレクトリ削除開始:' + StringOperation.toString(datetime.now().strftime("%Y-%m-%d")))

        for i in range(len(eList)):
            user_id = StringOperation.toString(eList[i])
            dirPath = Config.getConf('RECEIPTinfo', 'receipt_file_path') + user_id
            #年月は関係なし(ユーザーIDのディレクトリごとまるっと削除する)
            if os.path.isdir(dirPath):
                shutil.rmtree(dirPath)
                self.writeLog('ディレクトリ削除 ユーザーID: ' + user_id)

        self.writeLog('ディレクトリ削除完了:' + StringOperation.toString(datetime.now().strftime("%Y-%m-%d")))

    '''
    社員マスタデータを削除
    '''
    def deleteEmployeeData(self, ids):
        dao = EmployeeDao(self.db)

        dao.addWhereIn(EmployeeDao.COL_ID, ids)
        dao.doDelete()

        return