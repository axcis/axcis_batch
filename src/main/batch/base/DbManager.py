# coding: UTF-8
'''
DbManager
DBコネクション管理クラス

@author: takanori_gozu
'''
import mysql.connector
from src.main.batch.base.Config import Config

class DbManager:

    dbHost = None
    dbUser = None
    dbPassword = None
    dbSchema = None
    dbCharset = None

    conn = None
    st = None

    '''
    コンストラクタ
    '''
    def __init__(self):
        self.dbHost = Config.getConf('DBinfo', 'db_server')
        self.dbUser = Config.getConf('DBinfo', 'db_user')
        self.dbPassword = Config.getConf('DBinfo', 'db_password')
        self.dbSchema = Config.getConf('DBinfo', 'db_schema')
        self.dbCharset = Config.getConf('DBinfo', 'db_char')

    '''
    DB接続
    '''
    def connect(self):
        self.conn = mysql.connector.connect(user=self.dbUser, password=self.dbPassword, host=self.dbHost, database=self.dbSchema)
        self.st = self.conn.cursor(dictionary=True)

    '''
    select
    '''
    def select(self, sql):
        self.st.execute(sql)
        return self.st.fetchall()

    '''
    execute
    '''
    def execute(self, sql, autoCommit = True):
        self.st.execute(sql)
        if autoCommit == True:
            self.conn.commit()

    '''
    lastInsertId
    '''
    def getLastInsertId(self):
        return self.st.lastrowid()

    '''
    文字列のクオート処理
    '''
    def quote(self, val):
        return "'" + val + "'"

    '''
    トランザクション
    '''
    def commit(self):
        self.conn.commit()

    '''
    ロールバック
    '''
    def rollback(self):
        self.conn.rollback()

    '''
    DB切断
    '''
    def disConnect(self):
        if self.st != None:
            self.st = None
        if self.conn != None:
            self.conn = None