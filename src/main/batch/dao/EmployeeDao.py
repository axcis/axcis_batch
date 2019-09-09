# coding: UTF-8
'''
社員マスタテーブル定義ファイル

@author: takanori_gozu
'''
from src.main.batch.base.BaseDao import BaseDao

class EmployeeDao(BaseDao):

    TABLE_NAME = 'employee'

    COL_ID = 'id'
    COL_NAME = 'name'
    COL_LOGIN_ID = 'login_id'
    COL_PASSWORD = 'password'
    COL_EMAIL_ADDRESS = 'email_address'
    COL_USER_LEVEL = 'user_level'
    COL_DIVISION_ID = 'division_id'
    COL_HIRE_DATE = 'hire_date'
    COL_RETIREMENT = 'retirement'
    COL_RETIREMENT_DATE = 'retirement_date'
    COL_UPD_USER_ID = 'upd_user_id'
    COL_UPD_USER_NAME = 'upd_user_name'
    COL_UPD_DATETIME = 'upd_datetime'

    '''
    コンストラクタ
    '''
    def __init__(self, db):
        super(EmployeeDao, self).__init__(db, self.TABLE_NAME)
