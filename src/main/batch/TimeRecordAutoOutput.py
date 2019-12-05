# coding: UTF-8
'''
勤怠自動出力バッチ

@author: takanori_gozu
'''
import sys
from src.main.batch.base.BaseBatch import BaseBatch
from src.main.batch.logic.time_record.TimeRecordAutoOutputLogic import TimeRecordAutoOutputLogic

class TimeRecordAutoOutput(BaseBatch):

    appId = 'TimeRecordAutoOutput'
    appName = '勤怠自動出力バッチ'

    '''
    ロジック
    '''
    def getLogic(self, db, logger, form):
        logic = TimeRecordAutoOutputLogic(db, logger, form)
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
    batch = TimeRecordAutoOutput()
    batch.mainProc(sys.argv)