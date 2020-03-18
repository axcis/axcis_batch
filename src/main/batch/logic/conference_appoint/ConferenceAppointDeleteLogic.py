# coding: UTF-8
'''
会議室予約状況データ削除バッチ処理ロジック

@author: takanori_gozu
'''
from src.main.batch.base.BaseLogic import BaseLogic
from src.main.batch.dao.ConferenceAppointDao import ConferenceAppointDao
from src.main.batch.lib.date.DateUtilLib import DateUtilLib
from src.main.batch.lib.string.StringOperationLib import StringOperationLib

class ConferenceAppointDeleteLogic(BaseLogic):

    '''
    コンストラクタ
    '''
    def __init__(self, db, logger, form):
        super(ConferenceAppointDeleteLogic, self).__init__(db, logger, form)

    '''
    run
    '''
    def run(self):
        date = self.getForm('-date')

        if date == '':
            self.writeLog('parameter:-date is not set')
            return

        #基準日を取得(3ヶ月保持)
        stdDate = self.getStandardDate(date)

        #過去データを削除する
        dao = ConferenceAppointDao(self.db)

        dao.addWhereStr(ConferenceAppointDao.COL_TARGET_DATE, stdDate, ConferenceAppointDao.COMP_LESS)

        count = dao.doCount()

        self.writeLog('削除対象データ件数：' + StringOperationLib.toString(count) + '件')

        dao.doDelete()

        return

    '''
    削除基準日を取得する(3ヶ月より前)
    '''
    def getStandardDate(self, dt):
        date = DateUtilLib.toDateTimeDate(dt)
        #文字列で返す
        return StringOperationLib.toString(DateUtilLib.getDateIntervalMonth(date, -3))