#!/usr/bin/python
# -*- coding:utf-8 -*-
import smtplib
from email.header import Header
from email.mime.text import MIMEText


class SendMail(object):
    def __init__(self, subject, value):
        self.host = 'host'
        self.from_addr = 'addr'
        self.pw = 'password'
        self.msg = self.makemsg(subject, value)

    @staticmethod
    def makemsg(subject, text):
        msg = MIMEText(text, 'plain', 'utf-8')
        msg['From'] = '123<123@sina.cn>'
        msg['To'] = '456<456@163.com>'
        msg['Subject'] = Header(u'预警:' + subject)
        return msg

    def send(self):
        server = smtplib.SMTP(self.host, 25)
        server.set_debuglevel(1)
        server.login(self.from_addr, self.pw)
        server.sendmail(self.from_addr, ['456@163.com'], self.msg.as_string())
        server.quit()


if __name__ == '__main__':
    sender = SendMail(u'压力测试', u'2017-7-19 21:00:00 压力值 999')
    sender.send()
