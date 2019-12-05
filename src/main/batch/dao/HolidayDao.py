# coding: UTF-8
'''
祝祭日マスタテーブル定義ファイル

@author: takanori_gozu
'''
from src.main.batch.base.BaseDao import BaseDao

class HolidayDao(BaseDao):

    TABLE_NAME = 'holiday'

    COL_HOLIDAY_DATE = 'holiday_date'
    COL_MONTH = 'month'
    COL_HOLIDAY_NAME = 'holiday_name'

    '''
    コンストラクタ
    '''
    def __init__(self, db):
        super(HolidayDao, self).__init__(db, self.TABLE_NAME)
