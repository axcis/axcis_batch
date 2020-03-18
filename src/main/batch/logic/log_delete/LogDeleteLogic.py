# coding: UTF-8
'''
ログファイル削除バッチ処理ロジック

@author: takanori_gozu
'''
from src.main.batch.base.BaseLogic import BaseLogic
from src.main.batch.base.Config import Config
from src.main.batch.lib.date.DateUtilLib import DateUtilLib
from src.main.batch.lib.file.FileOperationLib import FileOperationLib
from src.main.batch.lib.string.StringOperationLib import StringOperationLib

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

        for logPath in FileOperationLib.getFileList(dirPath, '*' + targetDate + '*.log'):
            FileOperationLib.deleteFile(logPath)
            count += 1

        self.writeLog('ログ削除件数:' + StringOperationLib.toString(count) + '件')

        return

    '''
    削除対象日を取得(60日前)
    '''
    def getTargetDate(self, dt, interval):
        date = DateUtilLib.toDateTimeDate(dt)
        return StringOperationLib.toString(DateUtilLib.getDateIntervalDay(date, -interval))