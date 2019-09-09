# coding: UTF-8
'''
お知らせデータ削除バッチ

@author: takanori_gozu
'''
import sys
from src.main.batch.base.BaseBatch import BaseBatch
from src.main.batch.logic.notice.NoticeDeleteLogic import NoticeDeleteLogic

class NoticeDelete(BaseBatch):

    appId = 'NoticeDelete'
    appName = 'お知らせデータ削除バッチ'

    '''
    ロジック
    '''
    def getLogic(self, db, logger, form):
        logic = NoticeDeleteLogic(db, logger, form)
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
    batch = NoticeDelete()
    batch.mainProc(sys.argv)