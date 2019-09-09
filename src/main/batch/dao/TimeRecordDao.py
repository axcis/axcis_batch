# coding: UTF-8
'''
勤怠データテーブル定義ファイル

@author: takanori_gozu
'''
from src.main.batch.base.BaseDao import BaseDao

class TimeRecordDao(BaseDao):

    TABLE_NAME = 'time_record'

    COL_EMPLOYEE_ID = 'employee_id'
    COL_WORK_DATE = 'work_date'
    COL_SCENE = 'scene'
    COL_CLASSIFICATION = 'classification'
    COL_START_TIME = 'start_time'
    COL_END_TIME = 'end_time'
    COL_BREAK_TIME = 'break_time'
    COL_PRESCRIBED_TIME = 'prescribed_time'
    COL_OVER_WORK_TIME = 'over_work_time'
    COL_MIDNIGHT_TIME = 'midnight_time'
    COL_MIDNIGHT_BREAK_TIME = 'midnight_break_time'
    COL_MIDNIGHT_OVER_WORK_TIME = 'midnight_over_work_time'
    COL_WORK_TIME = 'work_time'
    COL_REMARK = 'remark'

    '''
    コンストラクタ
    '''
    def __init__(self, db):
        super(TimeRecordDao, self).__init__(db, self.TABLE_NAME)