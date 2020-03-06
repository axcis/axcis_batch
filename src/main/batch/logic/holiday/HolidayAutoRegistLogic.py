# coding: UTF-8
'''
祝祭日データ自動登録バッチ処理ロジック(年次)

@author: takanori_gozu
'''
import jpholiday
from src.main.batch.base.BaseLogic import BaseLogic
from src.main.batch.dao.HolidayDao import HolidayDao
from src.main.batch.lib.string.StringOperation import StringOperation

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

        date = self.getForm('-date')

        if date == '':
            self.writeLog('parameter:-date is not set')
            return

        #対象年を取得
        targetYear = int(date[0:date.find('-')])

        #祝祭日一覧
        holidayList = jpholiday.year_holidays(targetYear)

        values =[]

        #BulkInsert処理
        for day in holidayList:
            holidayDate = StringOperation.toString(day[0])
            holidayMonth = StringOperation.toString(holidayDate[0:holidayDate.rfind('-')])
            holidayName = day[1]
            values.append([holidayDate,holidayMonth,holidayName])

        dao = HolidayDao(self.db)
        dao.addBulkCol(HolidayDao.COL_HOLIDAY_DATE)
        dao.addBulkCol(HolidayDao.COL_MONTH)
        dao.addBulkCol(HolidayDao.COL_HOLIDAY_NAME)
        dao.doBulkInsert(values)

        self.writeLog(StringOperation.toString(targetYear) + '年祝祭日データ登録完了')

        return