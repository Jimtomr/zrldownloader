#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import threading
import time
from urllib2 import urlopen
from sendmail import SendMail
from wxpy import *

class WatchDog(object):
    def __init__(self):
        self.target_url = ''.join(line.strip('\n') for line in open('target_url.txt', 'r').readlines())
        self.value = {}
        self.timestamp = 0
        # self.bot = Bot(cache_path=True)
        # self.chat = ensure_one(self.bot.groups().search(u'预警测试'))

    def monitor(self):
        target = urlopen(self.target_url).read()
        data = json.loads(target)
        info = []
        refresh_stauts = False
        for d in data:
            refresh_time, data_label, refresh_value = d['Time'].split('.')[0], d['TagName'].strip('ZRL_ZRL.'), \
                                                      d['Value']
            if data_label not in self.value.keys():
                print u'%s的WatchDog启动' % data_label
                self.value[data_label] = refresh_value
                print refresh_time, data_label, refresh_value
                refresh_stauts = True
            elif refresh_value != self.value[data_label]:
                print u'---------%s 发生变化---------' % data_label
                self.value[data_label] = refresh_value
                print u'已刷新：', refresh_time, data_label, refresh_value
                refresh_stauts = True
            info.append(' '.join([refresh_time, data_label + ':', refresh_value.split('.')[0]]))

        text = '\n'.join(info)
        print '##################### %s ###################\n' % data[0]['Time'].split('.')[0], \
            text
        timenow = time.time()

        if (refresh_stauts == True) and (timenow - self.timestamp > 60.0):
            if float(self.value[u'GX1排焦皮带排焦重量']) > 180.0:
                subject = u'GX1排焦皮带排焦重量达到' + self.value[u'GX1排焦皮带排焦重量'].split('.')[0]
                sender = SendMail(subject, text)
                sender.send()
                self.timestamp = timenow
            elif float(self.value[u'锅炉入口气体温度']) > 1000.0:
                subject = u'锅炉入口气体温度达到' + self.value[u'锅炉入口气体温度'].split('.')[0]
                sender = SendMail(subject, text)
                sender.send()
                self.timestamp = timenow
            elif float(self.value[u'主蒸汽流量']) > 100.0:
                subject = u'主蒸汽流量达到' + self.value[u'主蒸汽流量'].split('.')[0]
                sender = SendMail(subject, text)
                sender.send()
                self.timestamp = timenow

            # self.chat.send(text)
            # self.timestamp = timenow

    def refresh(self):
        try:
            self.monitor()
        except Exception as e:
            print u'刷新错误', e
        timer_in = threading.Timer(9, self.refresh)
        timer_in.start()


if __name__ == '__main__':
    dog = WatchDog()

    # timer_out = threading.Timer(1, dog.refresh)
    # timer_out.start()
    dog.refresh()
