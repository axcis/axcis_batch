# coding: UTF-8
'''
BaseBatch
バッチのBaseクラス

@author: takanori_gozu
'''

from datetime import datetime
from abc import ABCMeta, abstractmethod
from src.main.batch.base.DbManager import DbManager
from src.main.batch.base.BaseLogger import BaseLogger
from src.main.batch.base.Config import Config
from src.main.batch.lib.mail.SendMail import SendMail
from src.main.batch.lib.string.StringOperation import StringOperation

class BaseBatch(metaclass=ABCMeta):

    form = {} #フォーム(パラメータ)
    db = None   #DBコネクション情報
    logger = None #ロガー
    errLogger = None #エラー用ロガー
    conf = None

    logExt = ".log"

    procLogFileName = None #処理ログファイル名
    errLogFileName = None  #エラーログファイル名

    '''
    コンストラクタ
    '''
    def __init__(self):
        self.appId = self.getAppId()
        self.appName = self.getAppName()
        self.procLogFileName = self.appId + "_" + StringOperation.toString(datetime.now().strftime("%Y-%m-%d")) + self.logExt
        self.errLogFileName = self.appId + "_" + StringOperation.toString(datetime.now().strftime("%Y-%m-%d")) + "_Err" + self.logExt

    '''
    バッチのメイン処理
    '''
    def mainProc(self, args):

        try:

            '''
            実行引数を受け取る
            '''
            for num in range(len(args)):
                if num > 0:
                    if args[num][0] == '-':
                        key = args[num]
                        value = args[num + 1]
                        self.form[key] = value

            '''
            confファイルを読み込み
            '''
            Config.confLoad('system')

            '''
            ロガーオープン
            '''
            self.logger = BaseLogger(self.procLogFileName)
            self.logger.fileOpen()
            self.logger.writeLog("START_TIME=" + StringOperation.toString(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            self.logger.writeLog("START_BATCH_NAME=" + self.appName)
            self.logger.writeLog("PARAM_INFO=" + self.appId + " param:" + " ".join(args))

            '''
            DB接続
            '''
            self.db = DbManager()
            self.db.connect()

            '''
            ロジック実行
            '''
            logic = self.getLogic(self.db, self.logger, self.form)
            logic.run()
        except Exception as e:
            self.errProc(e)

        finally:
            self.db.disConnect()
            self.logger.writeLog("END_TIME=" + StringOperation.toString(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + '\r\n')
            self.logger.fileClose()

    def errProc(self, e):

        try:
            self.errLogger = BaseLogger(self.errLogFileName)
            self.errLogger.fileOpen()
            self.errLogger.writeErrLog(e)
            self.errLogger.fileClose()

            #エラーメール送信
            errMail = SendMail()

            errMail.setMailFrom(Config.getConf('MAILinfo', 'admin_mail_from'))
            errMail.setMailTo(Config.getConf('MAILinfo', 'admin_mail_to'))
            errMail.setErrMailSubject(self.appId)
            errMail.setErrMailText(self.appName, e)

            errMail.send()
        except Exception as e2:
            print(e2)

        finally:
            self.errLogger.fileClose()

    '''
    ロジック
    '''
    @abstractmethod
    def getLogic(self, db, logger, form):
        raise NotImplementedError

    '''
    アプリID
    '''
    @abstractmethod
    def getAppId(self):
        raise NotImplementedError

    '''
    アプリ名
    '''
    @abstractmethod
    def getAppName(self):
        raise NotImplementedError