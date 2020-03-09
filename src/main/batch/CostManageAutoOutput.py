# coding: UTF-8
'''
経費データ自動出力バッチ

@author: takanori_gozu
'''
import sys
from src.main.batch.base.BaseBatch import BaseBatch
from src.main.batch.logic.cost_manage.CostManageAutoOutputLogic import CostManageAutoOutputLogic

class CostManageAutoOutput(BaseBatch):

    appId = 'CostManageAutoOutput'
    appName = '経費データ自動出力バッチ'

    '''
    ロジック
    '''
    def getLogic(self, db, logger, form):
        logic = CostManageAutoOutputLogic(db, logger, form)
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
    batch = CostManageAutoOutput()
    batch.mainProc(sys.argv)