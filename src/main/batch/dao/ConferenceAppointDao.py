# coding: UTF-8
'''
会議室予約状況テーブル定義ファイル

@author: takanori_gozu
'''
from src.main.batch.base.BaseDao import BaseDao

class ConferenceAppointDao(BaseDao):

    TABLE_NAME = 'conference_appoint'

    COL_ID = 'id'
    COL_CONFERENCE_ID = 'conference_id'
    COL_TARGET_DATE = 'target_date'
    COL_START_TIME = 'start_time'
    COL_END_TIME = 'end_time'
    COL_REGIST_USER_ID = 'regist_user_id'
    COL_PURPOSE = 'purpose'

    '''
    コンストラクタ
    '''
    def __init__(self, db):
        super(ConferenceAppointDao, self).__init__(db, self.TABLE_NAME)