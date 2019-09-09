# coding: UTF-8
'''
BaseLogic
Logic処理のBaseクラス

@author: takanori_gozu
'''
from abc import ABCMeta, abstractmethod

class BaseLogic(metaclass=ABCMeta):

    db = None
    logger = None
    form = None

    '''
    コンストラクタ
    '''
    def __init__(self, db, logger, form):
        self.db = db
        self.logger = logger
        self.form = form

    '''
    ログ出力
    '''
    def writeLog(self, msg):
        self.logger.writeLog(msg)

    '''
    実行引数の取得
    '''
    def getForm(self, key, default = ''):
        if (key not in self.form):
            self.form[key] = default
            return default
        return self.form[key]

    @abstractmethod
    def run(self):
        raise NotImplementedError