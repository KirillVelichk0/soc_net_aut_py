import json
import smtplib as smtp
import sys, ssl
from email.mime.text import MIMEText
from email.header import Header
from pathlib import Path
class MailServer:
    def __init__(self):
        try:
            base_dir = Path(__file__).parent.parent.resolve()
            cur_path = base_dir.joinpath('configs', 'emailSenderConfig.json')
            with open(cur_path) as jConfig:
                configDict = json.load(jConfig)
                self.login = configDict['emailSenderLogin']
                pathToPass = configDict['pathToPass']
        except:
            sys.exit(3)
        with open(pathToPass) as file:
            lines = [line.rstrip() for line in file]
            self.password = lines[0]
        try:
            self.context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        except smtp.SMTPConnectError:
            return

    def Restart(self):
        try:
            self.context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            self.server = smtp.SMTP('smtp.yandex.ru', 587)
            self.server.starttls(context=self.context)
        except smtp.SMTPConnectError:
            return False
        try:
            self.server.login(self.login, self.password)
            return True
        except smtp.SMTPAuthenticationError:
            return False


    def TrySendToEmail(self, email:str, text:str):

        if not self.Restart():
            raise Exception()

        subject = 'Account registration'
        try:
           ''' mime = MIMEText(text, 'plain', 'utf-8')
            mime['Subject'] = Header(subject, 'utf-8')
            print(text)
            print(email)
            self.server.sendmail(self.login, email, mime.as_string())'''
           message = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(self.login,
                                                       email, 
                                                       subject, 
                                                       text)
           self.server.sendmail(self.login, email, message)
           self.server.quit()
        except:
            raise Exception()


   