# coding: UTF-8
'''
部署マスタテーブル定義ファイル

@author: takanori_gozu
'''
from src.main.batch.base.BaseDao import BaseDao

class DivisionDao(BaseDao):

    TABLE_NAME = 'division'

    COL_ID = 'id'
    COL_NAME = 'name'

    '''
    コンストラクタ
    '''
    def __init__(self, db):
        super(DivisionDao, self).__init__(db, self.TABLE_NAME)
