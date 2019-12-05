# coding: UTF-8
'''
SendMail
メール送信ライブラリ

@author: takanori_gozu
'''
import smtplib
from os.path import basename
from email import utils
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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
    mailAttach = []

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
        self.mailAttach = []

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
    添付ファイル
    '''
    def setAttach(self, path):
        self.mailAttach.append(path)

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
        self.message = MIMEMultipart()
        self.message['To'] = self.mailTo
        self.message['From'] = self.mailFrom
        self.message['Subject'] = self.mailSubject
        self.message['Date'] = utils.formatdate(localtime=True)
        self.message['Message-ID'] = utils.make_msgid()

        body = MIMEText(self.mailText.encode(self.charset), 'plain', self.charset)
        self.message.attach(body)

        for filePath in self.mailAttach:
            self.message.attach(self.attachment(filePath))

        self.smtp.sendmail(self.mailFrom, self.mailTo, self.message.as_string())
        self.smtp.close()


    '''
    添付ファイルの追加
    '''
    def attachment(self, path):

        # ファイルを添付
        with open(path, "rb") as f:
            part = MIMEApplication(f.read(), Name=basename(path))

        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(path)

        return part