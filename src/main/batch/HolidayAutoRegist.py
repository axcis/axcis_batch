# coding: UTF-8
'''
祝祭日データ自動登録バッチ(年次)

@author: takanori_gozu
'''
import sys
from src.main.batch.base.BaseBatch import BaseBatch
from src.main.batch.logic.holiday.HolidayAutoRegistLogic import HolidayAutoRegistLogic

class HolidayAutoRegist(BaseBatch):

    appId = 'HolidayAutoRegist'
    appName = '祝祭日データ自動登録バッチ'

    '''
    ロジック
    '''
    def getLogic(self, db, logger, form):
        logic = HolidayAutoRegistLogic(db, logger, form)
        return logic

    '''
    アプリID
    '''
    def getAppId(self):
        return self.appId

    '''
    アプリ名
    '''
    def getAppName(self):
        return self.appName

if __name__ == '__main__':
    batch = HolidayAutoRegist()
    batch.mainProc(sys.argv)