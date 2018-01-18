#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import threading
import time
import datetime
from urllib2 import urlopen
from wechatpy.enterprise import WeChatClient

proj_code = {u'长治':'ZRL_ZRL', u'光大':'02_SXGD_P1', u'朝川':'03_HNCC_P1'}
alert_value = json.loads(open('alert.json', 'r').read())

class WatchRobot(object):
    def __init__(self):
        self.target_url = ''.join(line.strip('\n') for line in open('target_url.txt', 'r').readlines())
        self.value = {}
        self.timestamp = 0
        self.bot = WeChatClient('CorpID', 'AES')
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
               # print u'开始监视 %s' % d['TagName']
                self.value[projcet_name][data_label] = refresh_value
               # print refresh_time, d['TagName'], refresh_value
                refresh_stauts = True
            elif refresh_value != self.value[projcet_name][data_label]:
               # print u'---------%s 发生变化---------' % d['TagName']
                self.value[projcet_name][data_label] = refresh_value
               # print u'已刷新：', refresh_time, d['TagName'], refresh_value
                refresh_stauts = True
            info[projcet_name].append(' '.join([refresh_time, data_label + ':', refresh_value[0:6]]))
        for key, value in info.items():
            self.text[key] = '\n'.join(value)
           # print '##################### %s ###################\n' % data[0]['Time'].split('.')[0], key + '\n'+self.text[key]

        alarm_starttime, alarm_endtime, current_time = (

            datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0, 0)),  # 8点开始报警
            datetime.datetime.combine(datetime.date.today(), datetime.time(21, 0, 0)),  # 21点停止报警
            datetime.datetime.now()  # 获取当前时间用于判断是否在8点到21点之间
        )
        present_timestamp = time.time()  # 获取当前时间戳用于控制报警间隔

        if (
                        (refresh_stauts is True) and
                        (300.0 < present_timestamp - self.timestamp) and
                    (alarm_starttime < current_time < alarm_endtime)
        ):

            for CDQ in proj_code.keys():
                # 高报
                for key, value in alert_value[u'H_Alert'][proj_code[CDQ]].items():
                    current_value = self.value[proj_code[CDQ]][key]
                    # print CDQ, key, value, current_value
                    if float(current_value) > value:
                        msg = u'%s：%s超过%s，当前值%s' % (CDQ, key, value, current_value[0:7])
                        self.bot.message.send_text(agent_id='1000002', user_ids='SanShi', content=msg, party_ids=u'')
                        self.timestamp = present_timestamp
                        # print msg
                # 低报
                for key, value in alert_value[u'L_Alert'][proj_code[CDQ]].items():
                    current_value = self.value[proj_code[CDQ]][key]
                    # print CDQ, key, value, current_value
                    if float(current_value) < value:
                        msg = u'%s：%s低于%s，当前值%s' % (CDQ, key, value, current_value[0:7])
                        self.bot.message.send_text(agent_id='1000002', user_ids='SanShi', content=msg, party_ids=u'')
                        self.timestamp = present_timestamp
                        # print msg


    def refresh(self):
        try:
            self.monitor()
        except Exception as e:
            print u'refresh error:', e
        timer_in = threading.Timer(9, self.refresh)
        timer_in.start()


if __name__ == '__main__':
    zrlrobot = WatchRobot()
    # zrlrobot.listener()
    zrlrobot.refresh()
    # embed()
