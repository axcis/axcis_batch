# coding: UTF-8
'''
祝祭日データ自動登録バッチ処理ロジック(年次)

@author: takanori_gozu
'''
from src.main.batch.base.BaseLogic import BaseLogic
from src.main.batch.dao.HolidayDao import HolidayDao
from src.main.batch.lib.date.DateUtilLib import DateUtilLib
from src.main.batch.lib.string.StringOperationLib import StringOperationLib

class HolidayAutoRegistLogic(BaseLogic):

    '''
    コンストラクタ
    '''
    def __init__(self, db, logger, form):
        super(HolidayAutoRegistLogic, self).__init__(db, logger, form)

    '''
    run
    '''
    def run(self):

        targetYear = self.getForm('-year')

        if targetYear == '':
            self.writeLog('parameter:-year is not set')
            return

        #祝祭日一覧
        holidayList = DateUtilLib.getHolidayList(StringOperationLib.toInt(targetYear))

        values =[]

        #BulkInsert処理
        for day in holidayList:
            holidayDate = StringOperationLib.toString(day[0])
            holidayMonth = StringOperationLib.toString(holidayDate[0:holidayDate.rfind('-')])
            holidayName = DateUtilLib.getHolidayName(day[0])
            values.append([holidayDate,holidayMonth,holidayName])

        dao = HolidayDao(self.db)
        dao.addBulkCol(HolidayDao.COL_HOLIDAY_DATE)
        dao.addBulkCol(HolidayDao.COL_MONTH)
        dao.addBulkCol(HolidayDao.COL_HOLIDAY_NAME)
        dao.doBulkInsert(values)

        self.writeLog(targetYear + '年祝祭日データ登録完了')

        return