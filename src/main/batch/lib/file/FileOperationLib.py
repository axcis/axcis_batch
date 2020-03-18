# coding: UTF-8
'''
FileOperationLib
ファイル操作関数ライブラリ

@author: takanori_gozu
'''

import os
import shutil
import glob

class FileOperationLib:

    '''
    ファイルの存在チェック
    '''
    @staticmethod
    def existFile(path):
        return os.path.isfile(path)

    '''
    ディレクトリの存在チェック
    '''
    @staticmethod
    def existDir(path):
        return os.path.isdir(path)

    '''
    ファイル名を取得
    '''
    @staticmethod
    def getFileName(path):
        return os.path.basename(path)

    '''
    ファイルの削除
    '''
    @staticmethod
    def deleteFile(path):
        os.remove(path)

    '''
    ディレクトリの作成
    '''
    @staticmethod
    def makeDir(path):
        os.mkdir(path)

    '''
    ディレクトリの削除
    '''
    @staticmethod
    def deleteDir(path):
        shutil.rmtree(path)

    '''
    ファイルのコピー
    '''
    @staticmethod
    def copyFile(fromPath, toPath):
        shutil.copyfile(fromPath, toPath)

    '''
    サブディレクトリ一覧を取得
    '''
    @staticmethod
    def getSubDirList(path):
        return glob.glob(path + '*')

    '''
    ディレクトリ内のファイル一覧を取得
    '''
    @staticmethod
    def getFileList(path, pattern = '*'):
        return glob.glob(path + pattern)

    '''
    圧縮ファイルの作成
    '''
    @staticmethod
    def fileArchive(fileName, outputPath, basePath, type = 'zip'):
        shutil.make_archive(outputPath + fileName, type, root_dir=basePath)