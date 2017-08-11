#!/usr/bin/python
# -*- coding:utf-8 -*-
# 20170628update:主要功能封装到类中
# 20170724update:改为从外部读取基础url，改为更python风格的代码

import urllib
import time
import datetime
from mkcurve4 import AutoMaker


class DailyDownloader(object):
    def __init__(self, locallist, device):
        self.url = self.makeurl(locallist)
        self.filename = self.makefilename(device)

    def download(self):
        urllib.urlretrieve(self.url, self.filename)

    @staticmethod
    def makeurl(locallist):
        key = 11644473600434
        yesterday = datetime.date.today() + datetime.timedelta(days=-1)
        begin_time = time.mktime(datetime.datetime.combine(yesterday, datetime.time.min).timetuple())
        end_time = time.mktime(datetime.datetime.combine(yesterday, datetime.time.max).timetuple())
        begin_id = (int(begin_time) * 1000 + key) * 10000
        end_id = (int(end_time) * 1000 + key) * 10000

        pointlist = open(locallist, 'r').readlines()
        points = ';'.join('zrl_zrl.' + urllib.quote(line.rstrip('\n')) for line in pointlist[1:])
        url = pointlist[0].rstrip('\n') % (begin_id, end_id) + points
        print url
        return url

    @staticmethod
    def makefilename(device):
        date = datetime.date.today() + datetime.timedelta(days=-1)
        date_s = date.strftime("%Y-%m-%d")
        filename = date_s + device + '.xls'
        return filename


if __name__ == '__main__':
    CDQdownloader = DailyDownloader('CDQlist.txt', 'CDQ')
    CDQdownloader.download()

    maker = AutoMaker(CDQdownloader.filename, [1, 5, 9])
    maker.draw()

    Boilerdownloader = DailyDownloader('Boilerlist.txt', 'Boiler')
    Boilerdownloader.download()

    maker2 = AutoMaker(Boilerdownloader.filename, [1, 5, 9])
    maker2.draw()