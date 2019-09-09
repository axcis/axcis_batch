# coding: UTF-8
'''
週報データ削除バッチ

@author: takanori_gozu
'''
import sys
from src.main.batch.base.BaseBatch import BaseBatch

class WeeklyReportDelete(BaseBatch):

    appId = 'WeeklyReportDelete'
    appName = '週報データ削除バッチ'

    '''
    ロジック
    '''
    def getLogic(self, db, logger, form):
        logic = WeeklyReportDeleteLogic(db, logger, form)
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
    batch = WeeklyReportDelete()
    batch.mainProc(sys.argv)