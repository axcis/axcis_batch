# coding: UTF-8
'''
社内研修解答状況データ削除バッチ

@author: takanori_gozu
'''
import sys
from src.main.batch.base.BaseBatch import BaseBatch
from src.main.batch.logic.training.TrainingAnswerDeleteLogic import TrainingAnswerDeleteLogic

class TrainingAnswerDelete(BaseBatch):

    appId = 'TrainingAnswerDelete'
    appName = '社内研修解答状況データ削除バッチ'

    '''
    ロジック
    '''
    def getLogic(self, db, logger, form):
        logic = TrainingAnswerDeleteLogic(db, logger, form)
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
    batch = TrainingAnswerDelete()
    batch.mainProc(sys.argv)