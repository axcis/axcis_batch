# coding: UTF-8
'''
勤怠設定テーブル定義ファイル

@author: takanori_gozu
'''
from src.main.batch.base.BaseDao import BaseDao

class TimeRecordConfigDao(BaseDao):

    TABLE_NAME = 'time_record_config'

    COL_EMPLOYEE_ID = 'employee_id'
    COL_START_TIME = 'start_time'
    COL_END_TIME = 'end_time'
    COL_BREAK_TIME = 'break_time'
    COL_MIDNIGHT_BREAK_TIME = 'midnight_break_time'
    COL_PRESCRIBED_TIME = 'prescribed_time'

    '''
    コンストラクタ
    '''
    def __init__(self, db):
        super(TimeRecordConfigDao, self).__init__(db, self.TABLE_NAME)