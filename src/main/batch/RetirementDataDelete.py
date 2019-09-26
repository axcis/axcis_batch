# coding: UTF-8
'''
退職者データ削除バッチ

@author: takanori_gozu
'''
import sys
from src.main.batch.base.BaseBatch import BaseBatch
from src.main.batch.logic.retirement.RetirementDataDeleteLogic import RetirementDataDeleteLogic

class RetirementDataDelete(BaseBatch):

    appId = 'RetirementDataDelete'
    appName = '退職者データ削除バッチ'

    '''
    ロジック
    '''
    def getLogic(self, db, logger, form):
        logic = RetirementDataDeleteLogic(db, logger, form)
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
    batch = RetirementDataDelete()
    batch.mainProc(sys.argv)