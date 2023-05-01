import json
import smtplib as smtp
import sys
from email.mime.text import MIMEText
from email.header import Header

class MailServer:
    def __init__(self):
        try:
            with open('../configs/emailSenderConfig.json') as jConfig:
                configDict = json.load(jConfig)
                self.login = configDict['emailSenderLogin']
                pathToPass = configDict['pathToPass']
        except:
            sys.exit(3)
        with open(pathToPass) as file:
            lines = [line.rstrip() for line in file]
            password = lines[0]
        try:
            self.server = smtp.SMTP_SSL('smtp.yandex.ru', 587)
        except smtp.SMTPConnectError:
            sys.exit(1)
        self.server.starttls()
        try:
            self.server.login(self.login, password)
        except smtp.SMTPAuthenticationError:
            sys.exit(2)


    def TrySendToEmail(self, email:str, text:str):
        subject = 'Account registration'
        try:
            mime = MIMEText(text, 'plain', 'utf-8')
            mime['Subject'] = Header(subject, 'utf-8')
            self.server.sendmail(self.login, email, mime.as_string())
        except:
            sys.exit(4)


   