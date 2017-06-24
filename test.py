#!/usr/bin/env python
#encoding=utf-8

from apscheduler.schedulers.blocking import BlockingScheduler
from tool.weather import Weather
from tool.edbus import Edbus
from tool.evcard import Evcard
from config import CITY
from pinyin.pinyin import PinYin

def test():
    ev = Evcard()
    # ev.getCityList()
    ev.saveToMongo()

    ev.save()

    ev.upload()


    # ev.setAreaCodeList()
    # ev.testCron()
    # print('hello,world')

if __name__ == '__main__':
    test()
    # sched = BlockingScheduler()
    # sched.add_job(test,'cron',hour=22,minute = 31)
    # sched.start()










# import pymongo
# import json
#
# from datetime import date
#
# client = pymongo.MongoClient('localhost')
# db = client['evcard']
# today = date.today().strftime('%Y-%m-%d')
# print(today,type(today))
# data = db['AreaCodeList'].find_one({today:{'$exists':True}},{'_id':0})
# tmp = data.get(today)
#
# cityList = list(set([item.get('city') for item in tmp]))
# print(cityList)