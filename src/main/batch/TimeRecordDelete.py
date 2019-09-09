# coding: UTF-8
'''
勤怠データ削除バッチ

@author: takanori_gozu
'''
import sys
from src.main.batch.base.BaseBatch import BaseBatch
from src.main.batch.logic.time_record.TimeRecordDelete import TimeRecordDeleteLogic

class TimeRecordDelete(BaseBatch):

    appId = 'TimeRecordDelete'
    appName = '勤怠データ削除バッチ'

    '''
    ロジック
    '''
    def getLogic(self, db, logger, form):
        logic = TimeRecordDeleteLogic(db, logger, form)
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
    batch = TimeRecordDelete()
    batch.mainProc(sys.argv)