# coding: UTF-8
'''
お知らせデータ削除バッチ処理ロジック

@author: takanori_gozu
'''
from src.main.batch.base.BaseLogic import BaseLogic
from src.main.batch.dao.NoticeDao import NoticeDao
from src.main.batch.dao.PresenceDao import PresenceDao
from src.main.batch.lib.collection.CollectionLib import CollectionLib
from src.main.batch.lib.string.StringOperationLib import StringOperationLib

class NoticeDeleteLogic(BaseLogic):

    '''
    コンストラクタ
    '''
    def __init__(self, db, logger, form):
        super(NoticeDeleteLogic, self).__init__(db, logger, form)

    '''
    run
    '''
    def run(self):
        date = self.getForm('-date')

        if date == '':
            self.writeLog('parameter:-date is not set')
            return

        #掲載期限切れデータの情報を取得
        ids = self.getDeleteTargetData(date)

        if len(ids) == 0:
            self.writeLog('削除対象データなし')
            return

        self.writeLog('データ削除実施日：' + StringOperationLib.toString(date))

        #掲載期限切れデータを削除
        self.deleteNoticeData(ids)

        #付随する出欠確認データを削除
        self.deletePresenceData(ids)

        return

    '''
    掲載期限切れデータを取得
    '''
    def getDeleteTargetData(self, dt):
        dao = NoticeDao(self.db)

        dao.addSelect(NoticeDao.COL_ID)
        dao.addWhereStr(NoticeDao.COL_PUBLISHED_DATE, dt, NoticeDao.COMP_LESS)

        return CollectionLib.toStringList(dao.doSelect())

    '''
    お知らせデータを削除する
    '''
    def deleteNoticeData(self, ids):
        dao = NoticeDao(self.db)

        dao.addWhereIn(NoticeDao.COL_ID, ids)

        count = dao.doCount()

        self.writeLog('お知らせ削除対象データ件数：' + StringOperationLib.toString(count) + '件')

        dao.doDelete()

        return

    '''
    削除対象のお知らせに付随する出欠データを削除する
    '''
    def deletePresenceData(self, ids):
        dao = PresenceDao(self.db)

        dao.addWhereIn(PresenceDao.COL_NOTICE_ID, ids)

        count = dao.doCount()

        self.writeLog('出欠状況削除対象データ件数：' + StringOperationLib.toString(count) + '件')

        dao.doDelete()

        return