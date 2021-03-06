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
        # self.timestamp = 0
        self.bot = Bot(cache_path=True, console_qr=1)
        self.chat = ensure_one(self.bot.groups().search(u'预警测试'))
        # self.text = u'尚未获取数据，请稍后再试'
        self.text = {}

    def monitor(self):
        target = urlopen(self.target_url).read()
        data = json.loads(target)
        info = {}
        refresh_stauts = False
        for d in data:
            refresh_time, projcet_name, data_label, refresh_value = d['Time'].split('.')[0], d['TagName'].split('.')[0], \
                                                                    d['TagName'].split('.')[1],  d['Value']
            if projcet_name not in info.keys():
                info[projcet_name] = []
            if projcet_name not in self.value.keys():
                self.value[projcet_name] = {}
            if data_label not in self.value[projcet_name].keys():
                print u'开始监视 %s' % d['TagName']
                self.value[projcet_name][data_label] = refresh_value
                print refresh_time, d['TagName'], refresh_value
                refresh_stauts = True
            elif refresh_value != self.value[projcet_name][data_label]:
                print u'---------%s 发生变化---------' % d['TagName']
                self.value[projcet_name][data_label] = refresh_value
                print u'已刷新：', refresh_time, d['TagName'], refresh_value
                refresh_stauts = True
            info[projcet_name].append(' '.join([refresh_time, data_label + ':', refresh_value[0:6]]))
        for key in info.keys():
            self.text[key] = '\n'.join(info[key])
            print '##################### %s ###################\n' % data[0]['Time'].split('.')[0], key + '\n'+self.text[key]

        # alarm_starttime, alarm_endtime, current_time = (
        #
        #     datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0, 0)),  # 8点开始报警
        #     datetime.datetime.combine(datetime.date.today(), datetime.time(21, 0, 0)),  # 21点停止报警
        #     datetime.datetime.now()  # 获取当前时间用于判断是否在8点到21点之间
        # )
        # present_timestamp = time.time()  # 获取当前时间戳用于控制报警间隔
        #
        # if (  # to do 此段重复代码过多，考虑复用方法
        #                 (refresh_stauts is True) and
        #                 (300.0 < present_timestamp - self.timestamp) and
        #             (alarm_starttime < current_time < alarm_endtime)
        # ):
        #     if float(self.value[u'GX1排焦皮带排焦重量']) > 195.0:
        #         subject = u'预警：GX1排焦皮带排焦重量达到%s' % self.value[u'GX1排焦皮带排焦重量'][0:6]
        #         self.chat.send(subject)
        #         self.timestamp = present_timestamp
        #     if float(self.value[u'锅炉入口气体温度']) > 1000.0:
        #         subject = u'预警：锅炉入口气体温度达到%s' % self.value[u'锅炉入口气体温度'][0:6]
        #         self.chat.send(subject)
        #         self.timestamp = present_timestamp
        #     if float(self.value[u'锅炉入口气体压力']) < -1.0:
        #         subject = u'预警：锅炉入口气体压力达到%s' % self.value[u'锅炉入口气体压力'][0:6]
        #         self.chat.send(subject)
        #         self.timestamp = present_timestamp
        #     if float(self.value[u'主蒸汽流量']) > 100.0:
        #         subject = u'预警：主蒸汽流量达到%s' % self.value[u'主蒸汽流量'][0:6]
        #         self.chat.send(subject)
        #         self.timestamp = present_timestamp
        # self.text = text

    def listener(self):
        @self.bot.register(Group, TEXT)
        def print_group_msg(msg):
            if msg.is_at:
                print(msg)
                if u'长治' in msg:
                    msg.reply(self.text['ZRL_ZRL'])
                if u'光大' in msg:
                    msg.reply(self.text['02_SXGD_P1'])

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
