# coding: UTF-8
'''
勤怠データ削除バッチ処理ロジック

@author: takanori_gozu
'''
from datetime import datetime
from dateutil.relativedelta import relativedelta
from src.main.batch.base.BaseLogic import BaseLogic
from src.main.batch.lib.string.StringOperation import StringOperation
from src.main.batch.dao.TimeRecordDao import TimeRecordDao

class TimeRecordDeleteLogic(BaseLogic):

    '''
    コンストラクタ
    '''
    def __init__(self, db, logger, form):
        super(TimeRecordDeleteLogic, self).__init__(db, logger, form)

    '''
    run
    '''
    def run(self):
        date = self.getForm('-date')

        if date == '':
            self.writeLog('parameter:-date is not set')
            return

        stdDate = self.getStandardDate(date)

        self.writeLog('削除基準日：' + stdDate)

        dao = TimeRecordDao(self.db)

        dao.addWhereStr(TimeRecordDao.COL_WORK_DATE, stdDate, TimeRecordDao.COMP_LESS)

        count = dao.doCount()

        self.writeLog('削除対象データ件数：' + StringOperation.toString(count) + '件')

        dao.doDelete()

        return

    '''
    データ削除の基準日を取得する
    '''
    def getStandardDate(self, dt):
        date = dt + ' 00:00:00'
        bdt = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

        #文字列で返す
        return StringOperation.toString((bdt - relativedelta(years=3)).date())