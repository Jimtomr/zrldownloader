#!/usr/bin/python
# -*- coding:utf-8 -*-
# 20170712update：使用pandas读取excel文件。
# 20170811update：画图前先用replace和resample处理数据。
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from numpy import nan as NA
import os
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


class AutoMaker(object):
    def __init__(self, filename, data_id):
        self.filename = filename
        self.data_id = data_id

    def draw(self):
        data = pd.read_excel(self.filename)
        time_label = data.columns[0]
        # 给数据框指定新索引，替换0为空值，并重新采样
        data_res = data.set_index(time_label, drop=True).replace(0, NA).resample('5t').mean()
        date = data[time_label][1].strftime("%Y-%m-%d")
        for d in self.data_id:
            column_label = data.columns[d]
            fig = plt.figure(facecolor='white')
            ax = fig.add_subplot(1, 1, 1, facecolor='white')  # 也可以用RGB色号比如#F0FFFF
            fig.set_size_inches(16, 10)
            ax.plot(data[time_label], [data[column_label].mean()] * len(data[column_label]),
                    label=u'平均值',
                    color='r',
                    linestyle='dotted',
                    linewidth=1,
                    alpha=1)
            data_res.plot(y=column_label,
                      label=column_label.split('.')[1],
                      color='#1E90FF',
                      linestyle='solid',
                      linewidth=2,
                      alpha=1,
                      ax=ax)
            # ax.annotate('max', xytext=('1','2'),xy=(xtime[???, data[d].max()))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M:%S'))  # 设置时间显示格式
            ax.xaxis.set_major_locator(mdates.HourLocator([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]))  # 设置X轴显示哪几个时刻
            # ax.xaxis.grid(True)
            ax.yaxis.grid(True)
            ax.spines['bottom'].set_linewidth(1.5)
            ax.spines['top'].set_linewidth(0)
            ax.spines['left'].set_linewidth(1.5)
            ax.spines['right'].set_linewidth(0)
            ax.set_title(u'项目名称\n' + date, fontsize=20)
            ax.legend(loc='best')
            savedir = '.\\' + date + u'曲线'
            if not os.path.exists(savedir):
                os.makedirs(savedir)
            savename = savedir + '\\' + date + ' ' + column_label.split('.')[1] + '.pdf'
            print savename
            fig.savefig(savename, facecolor=fig.get_facecolor(), dpi=300, bbok_inches='tight')  # 保存到文件
            # plt.show()
            plt.close()


if __name__ == '__main__':
    sourcefile = '2017-07-13CDQ.xls'
    label_id = range(1,43)
    maker = AutoMaker(sourcefile, label_id)
    maker.draw()