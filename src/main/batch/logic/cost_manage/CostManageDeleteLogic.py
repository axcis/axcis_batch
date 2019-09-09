# coding: UTF-8
'''
経費データ削除バッチ処理ロジック

@author: takanori_gozu
'''
import os.path
import shutil
from datetime import datetime
from dateutil.relativedelta import relativedelta
from src.main.batch.base.BaseLogic import BaseLogic
from src.main.batch.lib.collection.Collection import Collection
from src.main.batch.dao.ExpensesDao import ExpensesDao
from src.main.batch.base.Config import Config
from src.main.batch.dao.EmployeeDao import EmployeeDao
from src.main.batch.lib.string.StringOperation import StringOperation

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
        date = dt + ' 00:00:00'
        bdt = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

        #文字列で返す
        return StringOperation.toString((bdt - relativedelta(years=3)).date())

    '''
    削除対象年月リストの取得
    '''
    def getDeleteTarget(self, dt):
        dao = ExpensesDao(self.db)

        dao.addSelectAs('left(regist_ymd, 7)', 'ym')
        dao.addWhereStr(ExpensesDao.COL_REGIST_YM, dt, ExpensesDao.COMP_LESS)
        dao.addGroupBy('ym')

        return Collection.toStringList(dao.doSelect(), 'ym')

    '''
    経費データの削除
    '''
    def deleteData(self, dt):
        self.writeLog('削除基準日:' + dt)

        dao = ExpensesDao(self.db)

        dao.addWhereStr(ExpensesDao.COL_REGIST_YM, dt, ExpensesDao.COMP_LESS)

        count = dao.doCount()

        self.writeLog('削除対象データ件数:' + StringOperation.toString(count) + '件')

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

        self.writeLog('ディレクトリ削除開始:' + StringOperation.toString(datetime.now().strftime("%Y-%m-%d")))

        for i in range(len(eList)):
            for j in range(len(arr)):
                ym = StringOperation.toString(StringOperation.left(arr[j], 4) + StringOperation.right(arr[j], 2))
                user_id = StringOperation.toString(eList[i])
                dirPath = Config.getConf('RECEIPTinfo', 'receipt_file_path') + user_id + '/' + ym
                if os.path.isdir(dirPath):
                    shutil.rmtree(dirPath)
                    self.writeLog('ディレクトリ削除 ユーザーID: ' + user_id + ' 対象年月: ' + ym)

        self.writeLog('ディレクトリ削除完了:' + StringOperation.toString(datetime.now().strftime("%Y-%m-%d")))