# coding: UTF-8
'''
社内研修解答状況テーブル定義ファイル

@author: takanori_gozu
'''
from src.main.batch.base.BaseDao import BaseDao

class TrainingQuestionAnswerDao(BaseDao):

    TABLE_NAME = 'training_question_answer'

    COL_EMPLOYEE_ID = 'employee_id'
    COL_TRAINING_TYPE = 'training_type'
    COL_POINT = 'point'
    COL_ANSWER_DATE = 'answer_date'

    '''
    コンストラクタ
    '''
    def __init__(self, db):
        super(TrainingQuestionAnswerDao, self).__init__(db, self.TABLE_NAME)
