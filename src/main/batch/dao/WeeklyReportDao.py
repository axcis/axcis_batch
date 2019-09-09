# coding: UTF-8
'''
週報テーブル定義ファイル

@author: takanori_gozu
'''
from src.main.batch.base.BaseDao import BaseDao

class WeeklyReportDao(BaseDao):

    TABLE_NAME = 'weekly_report'

    COL_ID = 'id'
    COL_REGIST_USER_ID = 'regist_user_id'
    COL_STANDARD_DATE = 'standard_date'
    COL_PROJECT_NAME = 'project_name'
    COL_WORK_CONTENT = 'work_content'
    COL_REFLECT = 'reflect'
    COL_OTHER = 'other'

    '''
    コンストラクタ
    '''
    def __init__(self, db):
        super(WeeklyReportDao, self).__init__(db, self.TABLE_NAME)
