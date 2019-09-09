# coding: UTF-8
'''
お知らせデータテーブル定義ファイル

@author: takanori_gozu
'''
from src.main.batch.base.BaseDao import BaseDao

class NoticeDao(BaseDao):

    TABLE_NAME = 'notice'

    COL_ID = 'id'
    COL_NOTICE_NAME = 'notice_name'
    COL_NOTICE_DETAIL = 'notice_detail'
    COL_IMPORTANT = 'important'
    COL_REGIST_DATE = 'regist_date'
    COL_PUBLISHED_DATE = 'published_date'
    COL_PRESENCE_CHK_FLG = 'presence_chk_flg'
    COL_PRESENCE_DATE = 'presence_date'

    '''
    コンストラクタ
    '''
    def __init__(self, db):
        super(NoticeDao, self).__init__(db, self.TABLE_NAME)