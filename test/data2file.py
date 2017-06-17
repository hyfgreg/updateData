import pymongo
import os
import requests
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
import json
from datetime import date
from tool.weather import Weather


#需要填写你的 Access Key 和 Secret Key
access_key = 'WxtU5PasZSCeEnuWZl_QtnlaIanDVSN7jO4s03HC'
secret_key = 'GeRvR9HYjmwaM75PilZumocBfmfnv7KboMFWVp1f'
#构建鉴权对象
q = Auth(access_key, secret_key)
#要上传的空间
bucket_name = 'yimove'


db = pymongo.MongoClient('127.0.0.1',27017) # pymongo存储天气和evcard等所有的数据
host = 'http://jisutqybmf.market.alicloudapi.com'
path1 = '/weather/city'
path2 = '/weather/query?'
def querys(id):
    return 'cityid='+str(id)

appcode = '6a4b15325da84f5bbef0e74a39987931'
headers = {"Authorization":"APPCODE 6a4b15325da84f5bbef0e74a39987931"}

myCollections = {
    'evcard':[
         'AreaCodeList',
         'ShopInfoList',
         'VehicleModeList'
    ]
}

city = [
    {'北京市':'Beijing'},{'上海市':'Shanghai'},{'广州市':'Guangzhou'}
]

# def getWeather():


def readData(dataBase,collection):
    data = db[dataBase][collection].find({},{'_id':0})
    #num = db[dataBase][collection].find({},{'_id':0}).count()
    for item in data:
        yield item

def saveData(data,filename=None,today = date.today().strftime('%Y-%m-%d')):
    try:
        if filename == None:
            print('请输入文件名！')
            return False
        file = os.getcwd()+'\\'+filename+today+'.json'
        #print(file)
        with open(file,'w',encoding='utf-8') as f:
            for item in data:
                #print(item)
                f.write(json.dumps(item,ensure_ascii=False,indent=4))
                f.write('\r')
        print('保存成功 ',file)
        return True
    except Exception as e:
        print(e.args)

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

def upload2qiniu(key = None,localfile=None):
    # 生成上传 Token，可以指定过期时间等
    try:
        if key == None:
            print('请输入保存的文件名')
            return False
        if localfile == None:
            print('请填写要上传的文档名')
            return False
        today = date.today().strftime('%Y-%m-%d')
        #token = q.upload_token(bucket_name, key, 3600)
        # 要上传文件的本地路径
        key = key+today+'.json'
        print(key)
        localfile = './'+localfile+today+'.json'
        print(localfile)
        token = q.upload_token(bucket_name, key, 3600)
        ret, info = put_file(token, key, localfile)
        print(info)
        assert ret['key'] == key
        assert ret['hash'] == etag(localfile)
        print('成功上传文档{}至{}'.format(localfile,bucket_name))
        return True
    except Exception as e:
        print(e.args)



def main():
    # for database,collections in myCollections.items():
    #     for collection in collections:
    #         data = readData(database,collection)
    #         saveData(data,filename=database+collection)
    #         upload2qiniu(key=database+collection,localfile=database+collection)
    #
    # for item in city:
    #     cityCHN = next(iter(item.keys()))
    #     cityENG = item.get(cityCHN)
    #     data = getCityShop(cityCHN)
    #     saveData(data,filename='evcard'+cityENG+'ShopInfoList')
    #     upload2qiniu(key = 'evcard'+cityENG+'ShopInfoList',localfile='evcard'+cityENG+'ShopInfoList')
    w = Weather('上海')
    w.upload()
    print(w.getCityWeather())



if __name__ == '__main__':
    main()