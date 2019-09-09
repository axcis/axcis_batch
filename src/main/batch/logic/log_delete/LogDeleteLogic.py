# coding: UTF-8
'''
ログファイル削除バッチ処理ロジック

@author: takanori_gozu
'''
import glob
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from src.main.batch.base.BaseLogic import BaseLogic
from src.main.batch.base.Config import Config
from src.main.batch.lib.string.StringOperation import StringOperation

class LogDeleteLogic(BaseLogic):

    '''
    コンストラクタ
    '''
    def __init__(self, db, logger, form):
        super(LogDeleteLogic, self).__init__(db, logger, form)

    '''
    run
    '''
    def run(self):
        date = self.getForm('-date')
        interval = int(self.getForm('-interval', 60))

        if date == '':
            self.writeLog('parameter:-date is not set')
            return

        targetDate = self.getTargetDate(date, interval)

        #パス取得
        dirPath = Config.getConf('LOGinfo', 'log_file_path')

        count = 0

        for i in glob.glob(dirPath + '*' + targetDate + '*.log'):
            os.remove(i)
            count+=1

        self.writeLog('ログ削除件数:' + StringOperation.toString(count) + '件')

        return

    '''
    削除対象日を取得(60日前)
    '''
    def getTargetDate(self, dt, interval):
        date = dt + ' 00:00:00'
        bdt = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

        #文字列で返す
        return StringOperation.toString((bdt - relativedelta(days=interval)).date())