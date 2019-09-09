# coding: UTF-8
'''
SendMail
メール送信ライブラリ

@author: takanori_gozu
'''
import smtplib
from email.mime.text import MIMEText
from src.main.batch.base.Config import Config
from src.main.batch.lib.string.StringOperation import StringOperation

class SendMail:

    message = None

    charset = 'ISO-2022-JP'

    mailFrom = None
    mailTo = None
    mailCc = None
    mailSubject = None
    mailText = None

    smtp = None

    '''
    コンストラクタ
    '''
    def __init__(self):
        self.reset()
        self.smtp = smtplib.SMTP(Config.getConf('MAILinfo', 'smtp_host'),
                                 Config.getConf('MAILinfo', 'smtp_port'),
                                 Config.getConf('MAILinfo', 'conn_timeout'))
        self.smtp.starttls()

    '''
    リセット
    '''
    def reset(self):
        self.smtp = None
        self.message = None
        self.mailFrom = None
        self.mailTo = None
        self.mailCc = None
        self.mailSubject = None
        self.mailText = None

    '''
    送信者
    '''
    def setMailFrom(self, mailFrom):
        self.mailFrom = mailFrom

    '''
    受信者
    '''
    def setMailTo(self, mailTo):
        self.mailTo = mailTo

    '''
    CC
    '''
    def setMailCc(self, mailCc):
        self.mailCc = mailCc

    '''
    件名
    '''
    def setMailSubject(self, mailSubject):
        self.mailSubject = mailSubject

    '''
    エラーメールの件名
    '''
    def setErrMailSubject(self, appId):
        self.mailSubject = u'【エラー発生】' + appId

    '''
    本文
    '''
    def setMailText(self, mailText):
        self.mailText = mailText

    '''
    エラーメールの本文
    '''
    def setErrMailText(self, appName, e):
        msg = appName + u'にてシステムエラーが発生しました。\r\n\r\n'
        msg += StringOperation.toString(e)
        self.mailText = msg

    '''
    送信
    '''
    def send(self):
        msg = MIMEText(self.mailText.encode(self.charset), 'plain', self.charset)
        msg['Subject'] = self.mailSubject
        msg['From'] = self.mailFrom
        msg['To'] = self.mailTo

        self.smtp.sendmail(self.mailFrom, self.mailTo, msg.as_string())
        self.smtp.close()