#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib
import time
import datetime
from SXGD_mkcurve import AutoMaker


class DailyDownloader(object):
    def __init__(self, locallist, device):
        self.date = datetime.date.today() + datetime.timedelta(days=-1)  # 获取昨天的日期
        self.url = self.makeurl(locallist)
        self.filename = self.makefilename(device)

    def download(self):
        urllib.urlretrieve(self.url, self.filename)

    def makeurl(self, locallist):
        key = 11644473600434
        begin_time = time.mktime(datetime.datetime.combine(self.date, datetime.time.min).timetuple())
        end_time = time.mktime(datetime.datetime.combine(self.date, datetime.time.max).timetuple())
        begin_id = (int(begin_time) * 1000 + key) * 10000
        end_id = (int(end_time) * 1000 + key) * 10000

        pointlist = open(locallist, 'r').readlines()
        points = ';'.join('02_SXGD_P1.' + urllib.quote(line.rstrip('\n')) for line in pointlist[1:])
        url = pointlist[0].rstrip('\n') % (begin_id, end_id) + points
        print url
        return url

    def makefilename(self, device):
        date_str = self.date.strftime("%Y-%m-%d")
        filename = date_str + device + '.xls'
        return filename

class ManualDownloader(DailyDownloader):
    def __init__(self, locallist, device):
        super(ManualDownloader, self).__init__(locallist, device)
        y, m, d = input('Input date like \'yyyy, m, d\': ')
        self.date = datetime.date(y, m, d)
        self.url = self.makeurl(locallist)
        self.filename = self.makefilename(device)

if __name__ == '__main__':
    # CDQdownloader = DailyDownloader('SXGD_CDQ.txt', 'CDQ')
    # CDQdownloader.download()
    #
    # maker = AutoMaker(CDQdownloader.filename, [1, 5, 9])
    # maker.draw()
    #
    # Boilerdownloader = DailyDownloader('SXGD_Boiler.txt', 'Boiler')
    # Boilerdownloader.download()
    #
    # maker2 = AutoMaker(Boilerdownloader.filename, [1, 5, 9])
    # maker2.draw()
    #
    # Cyclonedownloader = DailyDownloader('SXGD_Cyclone.txt', 'Cyclone')
    # Cyclonedownloader.download()
    #
    # maker3 = AutoMaker(Cyclonedownloader.filename, [1, 5, 9])
    # maker3.draw()

    Cyclonedownloader = ManualDownloader('SXGD_Cyclone.txt', 'Cyclone')
    Cyclonedownloader.download()

    CDQdownloader = ManualDownloader('SXGD_CDQ.txt', 'CDQ')
    CDQdownloader.download()

    Boilerdownloader = ManualDownloader('SXGD_Boiler.txt', 'Boiler')
    Boilerdownloader.download()