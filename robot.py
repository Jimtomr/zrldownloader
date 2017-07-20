#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import threading
import time
from urllib2 import urlopen
from wxpy import *


class WatchRobot(object):
    def __init__(self):
        self.target_url = ''.join(line.strip('\n') for line in open('target_url.txt', 'r').readlines())
        self.value = {}
        self.timestamp = 0
        self.bot = Bot(cache_path=True)
        self.chat = ensure_one(self.bot.groups().search(u'预警测试'))
        self.text = u'尚未获取数据，请稍后再试'

    def monitor(self):
        target = urlopen(self.target_url).read()
        data = json.loads(target)
        info = []
        refresh_stauts = False
        for d in data:
            refresh_time, data_label, refresh_value = d['Time'].split('.')[0], d['TagName'].strip('ZRL_ZRL.'), \
                                                      d['Value']
            if data_label not in self.value.keys():
                print u'开始监视 %s' % data_label
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
        print '##################### %s ###################\n' % data[0]['Time'].split('.')[0], text
        moment_time = time.time()

        if (refresh_stauts is True) and (120.0 < moment_time - self.timestamp):  # to do 此段重复代码过多，考虑复用方法
            if float(self.value[u'GX1排焦皮带排焦重量']) > 180.0:
                subject = u'预警：GX1排焦皮带排焦重量达到' + self.value[u'GX1排焦皮带排焦重量'].split('.')[0]
                self.chat.send(subject)
                self.timestamp = moment_time
            elif float(self.value[u'锅炉入口气体温度']) > 1000.0:
                subject = u'预警：锅炉入口气体温度达到' + self.value[u'锅炉入口气体温度'].split('.')[0]
                self.chat.send(subject)
                self.timestamp = moment_time
            elif float(self.value[u'主蒸汽流量']) > 100.0:
                subject = u'预警：主蒸汽流量达到' + self.value[u'主蒸汽流量'].split('.')[0]
                self.chat.send(subject)
                self.timestamp = moment_time
        self.text = text

    def listener(self):
        @self.bot.register(Group, TEXT)
        def print_group_msg(msg):
            if msg.is_at:
                print(msg)
                msg.reply(self.text)
        try:
            print_group_msg()
        except Exception as e:
            print e

    def refresh(self):
        try:
            self.monitor()
        except Exception as e:
            print u'刷新错误', e
        timer_in = threading.Timer(9, self.refresh)
        timer_in.start()


if __name__ == '__main__':
    zrlrobot = WatchRobot()
    zrlrobot.listener()
    zrlrobot.refresh()
