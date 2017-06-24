from tool.weather import Weather
from tool.edbus import Edbus
from tool.evcard import Evcard
from config import CITY
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from pinyin.pinyin import PinYin
import pymongo

def main():
    for k,_ in CITY.items():
        w = Weather(k)
        w.save()
        w.upload()
        w.saveToMongo()

    ed = Edbus()
    ed.save()
    ed.upload()
    ed.saveToMongo()

    ev = Evcard()
    ev.saveToMongo()
    ev.save()
    ev.upload()


if __name__ == '__main__':
    sched = BlockingScheduler()
    client = pymongo.MongoClient(host='localhost')
    store = MongoDBJobStore(collection='version_1',database='sched',client=client)
    sched.add_jobstore(store)
    sched.add_job(main, 'cron', hour=0,minute=30)
    print('Job Start!!!')
    try:
        sched.start()
    except KeyboardInterrupt:
        sched.remove_all_jobs()
        client.close()