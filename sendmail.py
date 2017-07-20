#!/usr/bin/python
# -*- coding:utf-8 -*-
import smtplib
from email.header import Header
from email.mime.text import MIMEText


class SendMail(object):
    def __init__(self, subject, text):
        self.host = 'host'
        self.from_addr = 'addr'
        self.pw = 'pass'
        self.subject = subject
        self.msg = self.makemsg(subject, text)

    @staticmethod
    def makemsg(subject, text):
        msg = MIMEText(text, 'plain', 'utf-8')
        msg['From'] = 'Robot<@>'
        msg['To'] = 'addr1<>, addr2<>'
        msg['Subject'] = Header(u'预警:' + subject)
        return msg

    def send(self):
        try:
            server = smtplib.SMTP(self.host, 25)
            # server.set_debuglevel(1)
            server.login(self.from_addr, self.pw)
            server.sendmail(self.from_addr, ['addr1', 'addr2'], self.msg.as_string())
            server.quit()
            print u'%s，已发送预警邮件' % self.subject
        except Exception as e:
            print u'邮件发送失败', e


if __name__ == '__main__':
    sender = SendMail(u'功能测试', u'2017-7-1 00:00:00 测试数值 999')
    sender.send()
