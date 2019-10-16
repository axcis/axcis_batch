# coding: UTF-8
'''
StringOperation
文字列操作関数ライブラリ

@author: takanori_gozu
'''
from datetime import datetime

class StringOperation:

    '''
    Left関数
    '''
    @staticmethod
    def left(text, length):
        return text[:length]

    '''
    Right関数
    '''
    @staticmethod
    def right(text, length):
        return text[-length:]

    '''
    Mid関数
    '''
    @staticmethod
    def mid(text, start, length):
        return text[start-1:start+length-1]

    '''
    文字列に変換して返す
    '''
    @staticmethod
    def toString(obj):
        return str(obj)

    '''
    文字列型日付をDatetime型日付に変換して返す
    '''
    @staticmethod
    def toDateTimeDate(date):
        return datetime.strptime(date, '%Y-%m-%d')