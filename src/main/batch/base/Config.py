# coding: UTF-8
'''
Config
confファイルの読み込みクラス

@author: takanori_gozu
'''

import configparser

class Config:

    conf = None
    CONF_DIR = 'conf/'

    CONF_EXT = '.conf'

    '''
    confファイルの読み込み
    '''
    @staticmethod
    def confLoad(fileName):
        Config.conf = configparser.ConfigParser()
        Config.conf.read(Config.CONF_DIR + fileName + Config.CONF_EXT)

    '''
    値の取得
    '''
    @staticmethod
    def getConf(section, key):
        return Config.conf.get(section, key)
