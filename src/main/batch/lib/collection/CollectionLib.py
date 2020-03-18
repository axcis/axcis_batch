# coding: UTF-8
'''
CollectionLib
コレクション(配列、リスト等)操作ライブラリ

@author: takanori_gozu
'''

class CollectionLib:

    '''
    指定された項目名のListを生成
    '''
    @staticmethod
    def toStringList(select, col = 'id'):
        newList = []

        for i in range(len(select)):
            newList.append(select[i][col])

        return newList

    '''
    key => valueのMap生成
    '''
    @staticmethod
    def toMap(select, key = 'id', value = 'name'):
        newMap = {}
        for i in range(len(select)):
            mapKey = select[i][key]
            mapValue = select[i][value]
            newMap[mapKey] = mapValue

        return newMap

    '''
    二次元配列から1つのカラムを連結して返す
    '''
    @staticmethod
    def toStringVal(select, col = 'id', delim = ','):
        val = ''

        for i in range(len(select)):
            if val != '': val += delim
            val += select[i][col]

        return val