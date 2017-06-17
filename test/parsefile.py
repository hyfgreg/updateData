import pymongo
db = pymongo.MongoClient('127.0.0.1',27017) # pymongo存储天气和evcard等所有的数据

def getCityShop(city = None):
    try:
        if city == None:
            print('请输入城市')
            return False
        data = db['evcard']['ShopInfoList'].find({'address':{'$regex':'^'+city}},{'_id':0})
        for item in data:
            yield item
    except Exception:
        print(Exception.args)

if __name__ == '__main__':
    data = getCityShop('上海市')
    for item in data:
        print(item)