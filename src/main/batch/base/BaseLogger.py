# coding: UTF-8
'''
BaseLogger
ロガーのBaseクラス

@author: takanori_gozu
'''
from src.main.batch.base.Config import Config
from src.main.batch.lib.string.StringOperation import StringOperation

class BaseLogger(object):

    path = None

    fileName = None #ログ出力ファイル名
    file = None #書き込みファイル

    '''
    コンストラクタ
    '''
    def __init__(self, fileName):
        self.path = Config.getConf('LOGinfo', 'log_file_path')
        self.fileName = fileName

    '''
    ファイルオープン
    '''
    def fileOpen(self):
        self.file = open(self.path + self.fileName, 'a')

    '''
    ログ書き込み
    '''
    def writeLog(self, msg):
        self.file.write(msg + '\r\n')

    '''
    エラーログの書き込み
    '''
    def writeErrLog(self, e):
        self.file.write(StringOperation.toString(e) + '\r\n')

    '''
    ファイルクローズ
    '''
    def fileClose(self):
        if self.file != None:
            self.file.close()