# coding: UTF-8
'''
会議室予約状況データ削除バッチ

@author: takanori_gozu
'''
import sys
from src.main.batch.base.BaseBatch import BaseBatch
from src.main.batch.logic.conference_appoint.ConferenceAppointDeleteLogic import ConferenceAppointDeleteLogic

class ConferenceAppointDelete(BaseBatch):

    appId = 'ConferenceAppointDelete'
    appName = '会議室予約状況データ削除バッチ'

    '''
    ロジック
    '''
    def getLogic(self, db, logger, form):
        logic = ConferenceAppointDeleteLogic(db, logger, form)
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
    batch = ConferenceAppointDelete()
    batch.mainProc(sys.argv)