#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import threading
from urllib2 import urlopen


class WatchDog(object):
    def __init__(self):
        self.target_url = open('target_url.txt', 'r').read()
        self.value = {}

    def monitor(self):
        target = urlopen(self.target_url).read()
        data = json.loads(target)
        for d in data:
            refresh_time, data_label, refresh_value = d['Time'], d['TagName'].strip('ZRL_ZRL.'), \
                                                      d['Value']
            if not data_label in self.value.keys():
                print '%s WatchDog' % data_label
                self.value[data_label] = refresh_value
            elif refresh_value != self.value[data_label]:
                print '---------%s changed---------' % data_label
                self.value[data_label] = refresh_value
            print refresh_time, data_label, refresh_value
        # if float(self.value[u'GX1排焦皮带排焦重量']) > 140.0:
            # pass

    def refresh(self):
        self.monitor()
        timer = threading.Timer(2, self.refresh)
        timer.start()


if __name__ == '__main__':
    dog = WatchDog()
    timer = threading.Timer(2, dog.refresh)
    timer.start()
