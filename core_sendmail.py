#!/usr/bin/python
# -*- coding:utf-8 -*-
import smtplib
import logging
import pandas as pd
import numpy as np
from io import BytesIO
from ConfigParser import SafeConfigParser
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SendMail(object):
    def __init__(self, subject, text, attfiles, cfg_file):
        # 读取外部配置
        cfg = SafeConfigParser()
        cfg.read(cfg_file)
        self.host = cfg.get('server', 'host')
        self.from_addr = cfg.get('server', 'from_addr')
        self.pw = cfg.get('server', 'pw')
        self.to_addr = cfg.get('server', 'to_addr')
        self.local_dir = cfg.get('local', 'local_dir').decode('utf-8')
        self.subject = attfiles[0][0:10] + subject
        # 生成邮件
        self.msg = self.makemail(text, attfiles)

    def makemail(self, text, attfiles):
        # 带附件的邮件实例
        mail = MIMEMultipart()
        mail['From'] = 'Robot<canon@bjceee.net.cn>'
        mail['To'] = self.to_addr
        mail['Subject'] = Header(self.subject)
        # 邮件正文
        msg = MIMEText(text, 'plain', 'utf-8')
        mail.attach(msg)
        # 附件
        for f in attfiles:
            df_ori = pd.read_excel(self.local_dir + f, index_col=u'时间')
            df_res = df_ori.replace(0, np.nan).resample('5min').mean()
            bio = BytesIO()
            # By setting the 'engine' in the ExcelWriter constructor.
            writer = pd.ExcelWriter(bio, engine='xlwt')
            df_res.to_excel(writer, sheet_name='Sheet1')
            # Save the workbook
            writer.save()
            # Seek to the beginning and read to copy the workbook to a variable in memory
            bio.seek(0)
            workbook = bio.read()
            bio.close()

            att1 = MIMEText(workbook, 'base64', 'utf-8')
            att1["Content-Type"] = 'application/octet-stream'
            # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
            att1["Content-Disposition"] = 'attachment; filename="%s"' % f
            mail.attach(att1)
        return mail

    def send(self):
        logging.basicConfig(filename='sendmail.log',
                            format='%(asctime)s:%(levelname)s:%(message)s',
                            level=logging.DEBUG)
        try:
            server = smtplib.SMTP(self.host, 25)
            # server.set_debuglevel(1)
            server.login(self.from_addr, self.pw)
            server.sendmail(self.from_addr, self.to_addr.split(','), self.msg.as_string())
            server.quit()
            print u'%s，已发送邮件' % self.subject
        except Exception as e:
            print u'邮件发送失败，请查看log', e
            logging.exception(u'邮件发送出错:')


if __name__ == '__main__':
    attfiles = ['2017-10-17CDQ.xls', '2017-10-17Boiler.xls']
    sender = SendMail(u'IO TEST REPORT FORMS',
                      u'测试信息，无需回复，附件是5分钟报表，原始报表可在服务器查看',
                      attfiles,
                      '.\\core_config.ini')
    sender.send()