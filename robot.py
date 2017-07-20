#!/usr/bin/python
#-*- coding:utf-8 -*-

from wxpy import *

bot = Bot(cache_path = True)
found = bot.groups().search(u'预警测试')
grchat = ensure_one(found)
info = ['CDQ','Boiler','1DC','GCF','VF']
text = '\n'.join(info)

@bot.register(Group, TEXT)
def print_group_msg(msg):
    if msg.is_at:
        print(msg)
        msg.reply(text)
try:
    print_group_msg()
except Exception as e:
    print e

embed()