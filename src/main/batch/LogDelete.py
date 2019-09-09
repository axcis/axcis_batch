# coding: UTF-8
'''
ログファイル削除バッチ
ログ保存期間は60日

@author: takanori_gozu
'''
import sys
from src.main.batch.base.BaseBatch import BaseBatch
from src.main.batch.logic.log_delete.LogDeleteLogic import LogDeleteLogic

class LogDelete(BaseBatch):

    appId = 'LogDelete'
    appName = 'ログファイル削除バッチ'

    '''
    ロジック
    '''
    def getLogic(self, db, logger, form):
        logic = LogDeleteLogic(db, logger, form)
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
    batch = LogDelete()
    batch.mainProc(sys.argv)