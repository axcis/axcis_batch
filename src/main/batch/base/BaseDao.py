# coding: UTF-8
'''
BaseDao
DaoのBaseクラス

@author: takanori_gozu
'''
from src.main.batch.lib.string.StringOperation import StringOperation
from src.main.batch.lib.collection.Collection import Collection

class BaseDao(object):

    COMP_EQUAL = ' = '
    COMP_NOT_EQUAL = ' <> '
    COMP_GREATER = ' > '
    COMP_GREATER_EQUAL = ' >= '
    COMP_LESS = ' < '
    COMP_LESS_EQUAL = ' <= '

    ORDER_ASC = 'asc'
    ORDER_DESC = 'desc'

    JOIN_LEFT = ' LEFT JOIN'
    JOIN_INNER = ' INNER JOIN'

    db = None
    table = None

    distinct = False
    join = False
    joinOn = ''

    select = []
    where = []
    order = []
    group = []
    limit = 0
    colValMap = {}

    '''
     コンストラクタ
    '''
    def __init__(self, db, table):
        self.db = db
        self.table = table
        self.reset()

    '''
    変数の初期化
    '''
    def reset(self):
        self.distinct = False
        self.join = False
        self.joinOn = ''
        self.select = []
        self.where = []
        self.order = []
        self.group = []
        self.limit = 0
        self.colValMap = {}

    '''
    select
    '''
    def addSelect(self, col, table2 = ''):
        if table2 != '':
            self.select.append(table2 + '.' + col)
        else:
            self.select.append(col)

    def addSelectAs(self, col, As):
        self.select.append(col + ' AS ' + As)

    def addSelectSumAs(self, col, As):
        self.select.append('SUM(' + col + ') AS ' + As)

    def setDistinct(self, distinct):
        self.distinct = distinct

    '''
    join
    '''
    def addJoinOn(self, join, col1, col2, table2):
        self.join = True
        sql = join + table2 + ' ON '
        sql += self.table + '.' + col1 + self.COMP_EQUAL + table2 + '.' + col2
        self.joinOn = sql

    '''
    通常のSelect
    '''
    def doSelect(self):
        sql = self.makeSelectStatement()

        if len(self.where) > 0:
            sql += self.makeWhereStatement()

        if len(self.order) > 0:
            sql += self.makeOrderStatement()

        if len(self.group) > 0:
            sql += self.makeGroupByStatement()

        if self.limit > 0:
            sql += self.makeLimitStatement()

        return self.db.select(sql)

    '''
    1件のみ取得(Map)
    '''
    def doSelectInfo(self):
        result = self.doSelect()
        return result[0]

    '''
    特定項目のみ取得(List)
    '''
    def doSelectCol(self, col):
        result = self.doSelect()
        return Collection.toStringList(result, col)

    '''
    doSelectColの1件取得Ver
    '''
    def doSelectColInfo(self, col):
        result = self.doSelectCol(col)
        return result[0]

    def makeSelectStatement(self):
        sql = 'SELECT'
        if len(self.select) == 0:
            sql += ' *'
        else:
            sql += ' '
            for i in range(len(self.select)):
                if i > 0:
                    sql += ', '
                sql += self.select[i]

        sql += ' FROM ' + self.table

        if self.join == True:
            sql += self.joinOn

        return sql

    def doCount(self):
        sql = 'SELECT Count(*) AS Cnt FROM ' + self.table

        if len(self.where) > 0:
            sql += self.makeWhereStatement()

        result = self.db.select(sql)

        return result[0]['Cnt']

    '''
    where
    '''
    def addWhere(self, col, val, comp = COMP_EQUAL):
        self.where.append(col + comp + val)

    def addWhereStr(self, col, val, comp = COMP_EQUAL):
        self.where.append(col + comp + self.db.quote(val))

    def addWhereIn(self, col, values):
        sql = ' IN ('
        j = 0
        for i in range(len(values)):
            if j > 0:
                sql += ','

            sql += str(values[i])
            j += 1

        sql += ')'
        self.where.append(col + sql)

    def addWhereNotIn(self, col, values):
        sql = ' NOT IN ('
        j = 0
        for i in range(len(values)):
            if j > 0:
                sql += ','

            sql += str(values[i])
            j += 1

        sql += ')'
        self.where.append(col + sql)

    def addWhereStatement(self, where):
        self.where.append(where)

    def makeWhereStatement(self):
        sql = ' WHERE '
        for i in range(len(self.where)):
            if i > 0:
                sql += ' AND '
            sql += self.where[i]

        return sql

    '''
    order by
    '''
    def addOrder(self, col, order = ORDER_ASC):
        self.order.append(col + ' ' + order)

    def makeOrderStatement(self):
        sql = ' ORDER BY '
        for i in range(len(self.order)):
            if i > 0:
                sql += ', '
            sql += self.order[i]

        return sql

    '''
    group by
    '''
    def addGroupBy(self, col):
        self.group.append(col)

    def makeGroupByStatement(self):
        sql = ' GROUP BY '
        for i in range(len(self.group)):
            if i > 0:
                sql += ', '
            sql += self.group[i]

        return sql

    '''
    limit
    '''
    def addLimit(self, count):
        self.limit = count

    def makeLimitStatement(self):
        sql = ' LIMIT ' + self.limit
        return sql

    '''
    col_val
    '''
    def addColVal(self, col, val):
        self.colValMap[col] = val

    def addColValStr(self, col, val):
        self.colValMap[col] = self.db.quote(val)

    '''
    insert
    '''
    def doInsert(self, autoCommit = True):
        sql = self.makeInsertStatement()

        self.db.execute(sql, autoCommit)

        return self.db.getLastInsertId()

    def makeInsertStatement(self):
        sql = 'INSERT INTO ' + self.table + '('

        keys = list(self.colValMap.keys())
        for i in range(len(keys)):
            if i > 0:
                sql += ', '
            sql += keys[i]

        sql += ') VALUES ('

        values = list(self.colValMap.values())
        for i in range(len(values)):
            if i > 0:
                sql += ', '
            sql += StringOperation.toString(values[i])

        sql += ');'

        return sql

    '''
    update
    '''
    def doUpdate(self, autoCommit = True):
        sql = self.makeUpdateStatement()

        if len(self.where) > 0:
            sql += self.makeWhereStatement()

        self.db.execute(sql, autoCommit)

    def makeUpdateStatement(self):
        sql = 'UPDATE ' + self.table + ' SET '

        keys = list(self.colValMap.keys())
        for i in range(len(keys)):
            if i > 0:
                sql += ', '
            sql += keys[i] + self.COMP_EQUAL + StringOperation.toString(self.colValMap[keys[i]])

        return sql

    '''
    delete
    '''
    def doDelete(self, autoCommit = True):
        sql = self.makeDeleteStatement()

        if len(self.where) > 0:
            sql += self.makeWhereStatement()

        self.db.execute(sql, autoCommit)

    def makeDeleteStatement(self):
        sql = 'DELETE FROM ' + self.table

        return sql