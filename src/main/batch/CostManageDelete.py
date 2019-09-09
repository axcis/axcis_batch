# coding: UTF-8
'''
経費データ削除バッチ

@author: takanori_gozu
'''
import sys
from src.main.batch.base.BaseBatch import BaseBatch
from src.main.batch.logic.cost_manage.CostManageDeleteLogic import CostManageDeleteLogic

class CostManageDelete(BaseBatch):

    appId = 'CostManageDelete'
    appName = '経費データ削除バッチ'

    '''
    ロジック
    '''
    def getLogic(self, db, logger, form):
        logic = CostManageDeleteLogic(db, logger, form)
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
    batch = CostManageDelete()
    batch.mainProc(sys.argv)