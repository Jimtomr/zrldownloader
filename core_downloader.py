#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib
import time
import datetime
from ConfigParser import SafeConfigParser

class DailyDownloader(object):
    def __init__(self, locallist, device, cfg_file):
        self.cfg = SafeConfigParser()
        self.cfg.read(cfg_file)
        self.date = datetime.date.today() + datetime.timedelta(days=-1)  # 获取昨天的日期
        self.url = self.makeurl(locallist)
        self.filename = self.makefilename(device)

    def download(self):
        local_dir = self.cfg.get('local','local_dir').decode('utf-8')
        urllib.urlretrieve(self.url, local_dir + self.filename)

    def makeurl(self, locallist):
        key = 11644473600434
        begin_time = time.mktime(datetime.datetime.combine(self.date, datetime.time.min).timetuple())
        end_time = time.mktime(datetime.datetime.combine(self.date, datetime.time.max).timetuple())
        begin_id = (int(begin_time) * 1000 + key) * 10000
        end_id = (int(end_time) * 1000 + key) * 10000

        proj_head = self.cfg.get('local', 'proj_head')
        pointlist = open(locallist, 'r').readlines()
        points = ';'.join(proj_head + urllib.quote(line.rstrip('\n')) for line in pointlist[1:])
        url = pointlist[0].rstrip('\n') % (begin_id, end_id) + points
        print url
        return url

    def makefilename(self, device):
        date_str = self.date.strftime("%Y-%m-%d")
        filename = date_str + device + '.xls'
        return filename


class ManualDownloader(DailyDownloader):
    def __init__(self, locallist, device, cfg_file):
        super(ManualDownloader, self).__init__(locallist, device, cfg_file)
        y, m, d = input('Input date like \'yyyy, m, d\': ')
        self.date = datetime.date(y, m, d)
        self.url = self.makeurl(locallist)
        self.filename = self.makefilename(device)


if __name__ == '__main__':
    CDQdownloader = DailyDownloader('HNCC_CDQ.txt', 'CDQ', '.\\core_config.ini')
    CDQdownloader.download()
    #
    Boilerdownloader = DailyDownloader('HNCC_Boiler.txt', 'Boiler', '.\\core_config.ini')
    Boilerdownloader.download()
    #
    # Cyclonedownloader = DailyDownloader('SXGD_Cyclone.txt', 'Cyclone')
    # Cyclonedownloader.download()
    #
    # Cyclonedownloader = ManualDownloader('SXGD_Cyclone.txt', 'Cyclone')
    # Cyclonedownloader.download()
    #
    # CDQdownloader = ManualDownloader('SXGD_CDQ.txt', 'CDQ')
    # CDQdownloader.download()
    #
    # Boilerdownloader = ManualDownloader('SXGD_Boiler.txt', 'Boiler')
    # Boilerdownloader.download()
