# coding: UTF-8
'''
経費データテーブル定義ファイル

@author: takanori_gozu
'''
from src.main.batch.base.BaseDao import BaseDao

class ExpensesDao(BaseDao):

    TABLE_NAME = 'expenses'

    COL_ID = 'id'
    COL_EMPLOYEE_ID = 'employee_id'
    COL_EXPENSES_YMD = 'expenses_ymd'
    COL_REGIST_YM = 'regist_ym'
    COL_INPUT_TYPE = 'input_type'
    COL_PAY_TYPE = 'pay_type'
    COL_EXPENSES_TYPE = 'expenses_type'
    COL_TRANSPORT = 'transport'
    COL_FROM_PLACE = 'from_place'
    COL_TO_PLACE = 'to_place'
    COL_EXPENSES_DETAIL = 'expenses_detail'
    COL_COST = 'cost'
    COL_RECEIPT_FILE_NAME = 'receipt_file_name'

    '''
    コンストラクタ
    '''
    def __init__(self, db):
        super(ExpensesDao, self).__init__(db, self.TABLE_NAME)
