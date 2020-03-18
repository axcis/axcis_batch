# coding: UTF-8
'''
DateUtilLib
日付関数ライブラリ

@author: takanori_gozu
'''
import jpholiday
import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta
from src.main.batch.lib.string.StringOperationLib import StringOperationLib

class DateUtilLib:

    weekdayList = ['月', '火', '水', '木', '金', '土', '日', '祝']

    '''
    今日の日付を返す
    '''
    @staticmethod
    def getToday():
        return datetime.now().strftime("%Y-%m-%d")

    '''
    現在日時を返す
    '''
    @staticmethod
    def getTime():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    '''
    年を返す
    '''
    @staticmethod
    def getYear(date):
        return StringOperationLib.toInt(date.strftime("%Y"))

    '''
    月を返す
    '''
    @staticmethod
    def getMonth(date):
        return StringOperationLib.toInt(date.strftime("%m"))

    '''
    日を返す
    '''
    @staticmethod
    def getDay(date):
        return StringOperationLib.toInt(date.strftime("%d"))

    '''
    対象年月の月末を取得
    '''
    @staticmethod
    def getLastDay(year, month):
        _, lastDay = calendar.monthrange(year,month)
        return lastDay

    '''
    曜日名を返す
    '''
    @staticmethod
    def getWeekDayName(date):
        return DateUtilLib.weekdayList[date.weekday()]

    '''
    曜日(数値)を返す
    '''
    @staticmethod
    def getWeekDay(date):
        return date.weekday()

    '''
    年を加算(減算)して返す
    '''
    @staticmethod
    def getDateIntervalYear(date, interval = 0):
        return date + relativedelta(years=interval)

    '''
    月を加算(減算)して返す
    '''
    @staticmethod
    def getDateIntervalMonth(date, interval = 0):
        return date + relativedelta(months=interval)

    '''
    日を加算(減算)して返す
    '''
    @staticmethod
    def getDateIntervalDay(date, interval = 0):
        return date + relativedelta(days=interval)

    '''
    文字列型日付をDatetime型日付に変換して返す
    '''
    @staticmethod
    def toDateTimeDate(date):
        return datetime.strptime(date, '%Y-%m-%d').date()

    '''
    Datetime型日付を文字列型日付に変換
    '''
    @staticmethod
    def toStringDate(date):
        return StringOperationLib.toString(date)

    '''
    時間のフォーマット変換(int→H:m)
    '''
    @staticmethod
    def toHm(time):
        if time == None: return None
        h, m = divmod(time, 60)
        return StringOperationLib.toString(h) + ':' + StringOperationLib.toString(m).zfill(2)

    '''
    YYYY-MM-DD→YYYY年n月j日
    '''
    @staticmethod
    def getDateFormatJapanese(date):
        year = StringOperationLib.toString(StringOperationLib.left(date, 4)) + '年'
        month = StringOperationLib.toString(StringOperationLib.toInt(StringOperationLib.mid(date, 6, 2))) + '月'
        day = StringOperationLib.toString(StringOperationLib.toInt(StringOperationLib.right(date, 2))) + '日'
        return year + month + day

    '''
    YYYY-MM→YYYY年n月
    '''
    @staticmethod
    def getYmFormatJapanese(ym):
        year = StringOperationLib.toString(StringOperationLib.left(ym, 4)) + '年'
        month = StringOperationLib.toString(StringOperationLib.toInt(StringOperationLib.right(ym, 2))) + '月'
        return year + month

    '''
    年月日をlistで返す
    '''
    @staticmethod
    def splitYmd(date, delimiter = '-'):
        return date.split(delimiter)

    '''
    年月をlistで返す
    '''
    @staticmethod
    def splitYm(ym, delimiter = '-'):
        return ym.split(delimiter)


    '''
    祝祭日一覧をListで返す
    '''
    @staticmethod
    def getHolidayList(year):
        return jpholiday.year_holidays(year)

    '''
    祝祭日名を返す
    '''
    @staticmethod
    def getHolidayName(date):
        return jpholiday.is_holiday_name(date)