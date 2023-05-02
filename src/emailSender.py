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
            password = lines[0]
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            self.server = smtp.SMTP('smtp.yandex.ru', 587)
            self.server.starttls(context=context)
        except smtp.SMTPConnectError:
            sys.exit(1)
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


   