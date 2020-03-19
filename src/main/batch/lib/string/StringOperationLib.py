# coding: UTF-8
'''
StringOperationLib
文字列操作関数ライブラリ

@author: takanori_gozu
'''
import fnmatch

class StringOperationLib:

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
    trim関数
    '''
    @staticmethod
    def trim(text):
        return text.strip()

    '''
    文字列置換関数
    '''
    @staticmethod
    def replace(text, before, after):
        return text.replace(before, after)

    '''
    Match関数
    '''
    @staticmethod
    def match(target, pattern):
        return fnmatch.fnmatch(target, pattern)

    '''
    文字列に変換して返す
    '''
    @staticmethod
    def toString(obj):
        return str(obj)

    '''
    数値に変換して返す
    '''
    @staticmethod
    def toInt(obj):
        return int(obj)

    '''
    数値の0埋め
    '''
    @staticmethod
    def printF(obj, interval):
        return obj.zfill(interval)