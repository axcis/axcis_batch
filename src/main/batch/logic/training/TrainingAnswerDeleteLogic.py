# coding: UTF-8
'''
社内研修解答状況データ削除バッチ処理ロジック

@author: takanori_gozu
'''
from src.main.batch.base.BaseLogic import BaseLogic
from src.main.batch.dao.TrainingQuestionAnswerDao import TrainingQuestionAnswerDao
from src.main.batch.lib.string.StringOperation import StringOperation

class TrainingAnswerDeleteLogic(BaseLogic):

    '''
    コンストラクタ
    '''
    def __init__(self, db, logger, form):
        super(TrainingAnswerDeleteLogic, self).__init__(db, logger, form)

    '''
    run
    '''
    def run(self):
        date = self.getForm('-date')
        type = self.getForm('-type')

        if date == '':
            self.writeLog('parameter:-date is not set')
            return

        dao = TrainingQuestionAnswerDao(self.db)

        self.writeLog('データ削除実施日：' + StringOperation.toString(date))

        dao.addWhereStr(TrainingQuestionAnswerDao.COL_ANSWER_DATE, StringOperation.toString(date), TrainingQuestionAnswerDao.COMP_LESS)
        if type != '':
            dao.addWhereStr(TrainingQuestionAnswerDao.COL_TRAINING_TYPE, StringOperation.toString(type))

        dao.doDelete()

        return