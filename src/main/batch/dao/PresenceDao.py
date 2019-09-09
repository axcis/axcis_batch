# coding: UTF-8
'''
出欠確認データテーブル定義ファイル

@author: takanori_gozu
'''
from src.main.batch.base.BaseDao import BaseDao

class PresenceDao(BaseDao):

    TABLE_NAME = 'presence'

    COL_NOTICE_ID = 'notice_id'
    COL_EMPLOYEE_ID = 'employee_id'
    COL_ANSWER_DATE = 'answer_date'
    COL_ATTENDANT = 'attendant'
    COL_REASON = 'reason'

    '''
    コンストラクタ
    '''
    def __init__(self, db):
        super(PresenceDao, self).__init__(db, self.TABLE_NAME)