#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import threading
import time
import datetime
from urllib2 import urlopen
from wxpy import *


class WatchRobot(object):
    def __init__(self):
        self.target_url = ''.join(line.strip('\n') for line in open('target_url.txt', 'r').readlines())
        self.value = {}
        self.timestamp = 0
        self.bot = Bot(cache_path=True, console_qr=1)
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
            info.append(' '.join([refresh_time, data_label + ':', refresh_value[0:6]]))
        text = '\n'.join(info)
        print '##################### %s ###################\n' % data[0]['Time'].split('.')[0], text

        alarm_starttime, alarm_endtime, current_time = (

            datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0, 0)),  # 8点开始报警
            datetime.datetime.combine(datetime.date.today(), datetime.time(21, 0, 0)),  # 21点停止报警
            datetime.datetime.now()  # 获取当前时间用于判断是否在8点到21点之间
        )
        present_timestamp = time.time()  # 获取当前时间戳用于控制报警间隔

        if (  # to do 此段重复代码过多，考虑复用方法
                        (refresh_stauts is True) and
                        (300.0 < present_timestamp - self.timestamp) and
                    (alarm_starttime < current_time < alarm_endtime)
        ):
            if float(self.value[u'GX1排焦皮带排焦重量']) > 180.0:
                subject = u'预警：GX1排焦皮带排焦重量达到' + self.value[u'GX1排焦皮带排焦重量'][0:6]
                self.chat.send(subject)
                self.timestamp = present_timestamp
            elif float(self.value[u'锅炉入口气体温度']) > 1000.0:
                subject = u'预警：锅炉入口气体温度达到' + self.value[u'锅炉入口气体温度'][0:6]
                self.chat.send(subject)
                self.timestamp = present_timestamp
            elif float(self.value[u'锅炉入口气体压力']) < -1.0:
                subject = u'预警：锅炉入口气体压力达到' + self.value[u'锅炉入口气体压力'][0:6]
                self.chat.send(subject)
                self.timestamp = present_timestamp
            elif float(self.value[u'主蒸汽流量']) > 100.0:
                subject = u'预警：主蒸汽流量达到' + self.value[u'主蒸汽流量'].split('.')[0:6]
                self.chat.send(subject)
                self.timestamp = present_timestamp
        self.text = text

    def listener(self):
        @self.bot.register(Group, TEXT)
        def print_group_msg(msg):
            if msg.is_at:
                print(msg)
                msg.reply(self.text)

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
    embed()
