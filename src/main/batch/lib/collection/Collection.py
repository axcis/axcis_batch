# coding: UTF-8
'''
Collection
コレクション(配列、リスト等)操作ライブラリ

@author: takanori_gozu
'''

class Collection:

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