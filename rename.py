from config import *
from qiniu import BucketManager
import datetime
import pymongo
from pinyin.pinyin import PinYin

py = PinYin()
py.load_word()
client = pymongo.MongoClient('localhost')

def getDate():
   return str(datetime.date.today())

def upload(bucket, key, localfile):
    token = q.upload_token(bucket, key, 3600)

    ret, info = put_file(token, key, localfile)
    print(info)
    assert  ret['key'] == key
    assert  ret['hash'] == etag(localfile)

# 移动文档到不同的空间，也可以实现重命名的功能
def rename(oldBucket,oldKey,newBucket,newKey):
    # 初始化BucketManager
    bucket = BucketManager(q)
    # # 你要测试的空间， 并且这个key在你空间中存在
    # bucket_name = 'Bucket_Name'
    # key = 'python-logo.png'
    # # 将文件从文件key 移动到文件key2，可以实现文件的重命名 可以在不同bucket移动
    # key2 = 'python-logo2.png'
    ret, info = bucket.move(oldBucket, oldKey, newBucket, newKey)
    print(info)
    assert ret == {}

def weatherReanme():
    oldBucket = newBucket = 'yimove'
    citys = ['Beijing','Guangzhou','Shanghai']
    for city in citys:
        for day in range(11,14):
            oldKey = 'weather'+city+'2017-06-'+str(day)+'.json'
            newKey = 'weather/'+city+'2017-06-'+str(day)+'.json'
            rename(oldBucket,oldKey,newBucket,newKey)

def weatherMove():
    oldBucket = 'weather'
    newBucket = 'yimove'
    citys = ['Beijing', 'Guangzhou', 'Shanghai']
    for city in citys:
        for day in range(7, 10):
            if day<10:
                day = '0'+str(day)
            oldKey = 'weather' + city + '2017-07-' +str(day) + '.json'
            newKey = 'weather/' + city + '2017-07-' + str(day) + '.json'
            rename(oldBucket, oldKey, newBucket, newKey)

def edbusRouteListRename():
    today = datetime.date.today()
    oldBucket = newBucket = 'yimove'

    for i in range(2,21):
        oldDay = today - datetime.timedelta(i)
        oldKey = 'edbusRouteList'+str(oldDay)+'.json'
        newKey = 'edbus/RouteList'+str(oldDay)+'.json'
        # print(oldKey)
        rename(oldBucket,oldKey,newBucket,newKey)

def edbusRouteListMove():
    oldBucket = 'edbusroutelist'
    newBucket = 'yimove'
    for day in range(7,10):
        if day < 10:
            day = '0' + str(day)
        oldKey = 'edbusRouteList2017-07-' + str(day) + '.json'
        newKey = 'edbus/RouteList2017-07-' + str(day) + '.json'
        print(oldKey)
        print(newKey)
        try:
            rename(oldBucket, oldKey, newBucket, newKey)
        except Exception:
            pass

def edbusRouteStationListRename():
    today = datetime.date.today()
    oldBucket = newBucket = 'yimove'

    for i in range(2,21):
        oldDay = today - datetime.timedelta(i)
        oldKey = 'edbusRouteStationList'+str(oldDay)+'.json'
        newKey = 'edbus/RouteStationList'+str(oldDay)+'.json'
        # print(oldKey)
        rename(oldBucket,oldKey,newBucket,newKey)

def edbusRouteStationListMove():
    oldBucket = 'edbusroutestationlist'
    newBucket = 'yimove'
    for day in range(7,10):
        if day < 10:
            day = '0' + str(day)
        oldKey = 'edbusRouteStationList2017-07-' + str(day) + '.json'
        newKey = 'edbus/RouteStationList2017-07-' + str(day) + '.json'
        print(oldKey)
        print(newKey)
        try:
            rename(oldBucket, oldKey, newBucket, newKey)
        except Exception:
            pass

def evcardAreaCodeListRename():
    today = datetime.date.today()
    oldBucket = newBucket = 'yimove'

    for i in range(2,21):
        oldDay = today - datetime.timedelta(i)
        oldKey = 'evcardAreaCodeList'+str(oldDay)+'.json'
        newKey = 'evcard/AreaCodeList'+str(oldDay)+'.json'
        # print(oldKey)
        rename(oldBucket,oldKey,newBucket,newKey)

def evcardAreaCodeListMove():
    oldBucket = 'evcardareacodelist'
    newBucket = 'yimove'
    for day in range(7,10):
        if day < 10:
            day = '0' + str(day)
        oldKey = 'evcardAreaCodeList2017-07-' + str(day) + '.json'
        newKey = 'evcardAreaCodeList/R2017-07-' + str(day) + '.json'
        print(oldKey)
        print(newKey)
        try:
            rename(oldBucket, oldKey, newBucket, newKey)
        except Exception:
            pass


def evcardVehicleModeListRename():
    today = datetime.date.today()
    oldBucket = newBucket = 'yimove'

    for i in range(2, 21):
        oldDay = today - datetime.timedelta(i)
        oldKey = 'evcardVehicleModeList' + str(oldDay) + '.json'
        newKey = 'evcard/VehicleModeList' + str(oldDay) + '.json'
        # print(oldKey)
        rename(oldBucket, oldKey, newBucket, newKey)


def evcardVehicleModeListMove():
    oldBucket = 'evcardvehiclemodelist'
    newBucket = 'yimove'
    for day in range(7,10):
        if day < 10:
            day = '0' + str(day)
        oldKey = 'evcardVehicleModeList2017-07-' + str(day) + '.json'
        newKey = 'evcard/VehicleModeList2017-07-' + str(day) + '.json'
        print(oldKey)
        print(newKey)
        try:
            rename(oldBucket, oldKey, newBucket, newKey)
        except Exception:
            pass


def getCityList():
    db = client[MONGO_DB['evcard']]['AreaCodeList']
    # if not db.find_one({getDate(): {'$exists': True}}, {'_id': 0}):
    #     self.setAreaCodeList()
    #     self.saveAreaCodeListToMongo()
    # data = db.find_one({self.getDate():{'$exists':True}},{'_id':0})
    data = db.find_one({getDate(): {'$exists': True}}, {'_id': 0})
    # print(data)
    tmp = data.get(getDate())
    # print(tmp)
    cityList = list(set([item.get('city') for item in tmp]))
    cityListEn = []
    for item in cityList:
        nameL = py.hanzi2pinyin(item[:-1])
        if 'zhong' in nameL:
            nameL[nameL.index('zhong')] = 'chong'
        name = ''.join(nameL).capitalize()
        cityListEn.append(name)
    # print(cityList)
    # print(cityListEn)
    return cityListEn

def evcardShopInfoListRename():
    cityList = getCityList()
    today = datetime.date.today()
    oldBucket = newBucket = 'yimove'
    for city in cityList:
        for i in range(2, 21):
            oldDay = today - datetime.timedelta(i)
            oldKey = 'evcard'+ city + str(oldDay) + '.json'
            newKey = 'evcard/'+city + str(oldDay) + '.json'
            # print(oldKey)
            # print(oldKey)
            # print(newKey)
            try:
                rename(oldBucket, oldKey, newBucket, newKey)
            except Exception:
                pass

def evcardShopInfoListMove():
    cityList = getCityList()
    today = datetime.date.today()
    oldBucket = 'evcardcityshoplist'
    newBucket = 'yimove'
    for city in cityList:
        for day in range(7, 10):
            # oldDay = today - datetime.timedelta(i)
            day = '0'+str(day)
            oldKey = 'evcard'+ city + '2017-07-'+ day + '.json'
            newKey = 'evcard/'+ city + '2017-07-'+ day + '.json'
            # print(oldKey)
            print(oldKey)
            print(newKey)
            try:
                rename(oldBucket, oldKey, newBucket, newKey)
            except Exception:
                pass

def main():
    # oldBucket = 'yimove'
    # newBucket = 'yimove'
    #
    # oldKey = 'weather/Shanghai2017-06-13.json'
    # newKey = 'weatherShanghai2017-06-13.json'
    #
    # rename(oldBucket,oldKey,newBucket,newKey)
    # weatherReanme()
    # weatherMove()

    # edbusRouteStationListRename()

    # evcardAreaCodeListRename()
    # getCityList()
    # evcardVehicleModeListRename()

    # evcardShopInfoListRename()
    # edbusRouteStationListMove()

    # evcardAreaCodeListMove()
    # evcardShopInfoListMove()

    evcardVehicleModeListMove()
if __name__ == '__main__':
    main()