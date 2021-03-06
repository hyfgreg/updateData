import json
from collections import OrderedDict

import copy
import requests
import pymongo
import time
from requests.exceptions import RequestException
from datetime import date
from pinyin.pinyin import PinYin

from config import *

py = PinYin()
py.load_word()

class Evcard(object):
    def __init__(self):
        self._data = self.setData()
        #     {
        #         'AreaCodeList': [None, self.saveAreaCodeList,self.saveAreaCodeListToMongo,self.uploadAreaCodeList],
        #         'ShopInfoList': [None, self.saveCityShopInfoList,self.saveCityShopInfoListToMongo,self.uploadCityShopInfoList],
        #         'VehicleModeList': [None, self.saveVehicleModeList,self.saveVehicleModeListToMongo,self.uploadVehicleModeList]
        #     }
        # )
        self.cityDict = None
        self.cityList = None
        self.cityListEN = None
        self._client = self.setClient()

    def setData(self):
        data = OrderedDict()
        data['AreaCodeList'] = [None, self.saveAreaCodeList,self.saveAreaCodeListToMongo,self.uploadAreaCodeList]
        data['ShopInfoList'] = [None, self.saveCityShopInfoList,self.saveCityShopInfoListToMongo,self.uploadCityShopInfoList]
        data['VehicleModeList'] = [None, self.saveVehicleModeList,self.saveVehicleModeListToMongo,self.uploadVehicleModeList]
        return data

    def showData(self):
        for k,v in self._data.items():
            print(v[-3:])

    def setClient(self):
        return pymongo.MongoClient(MONGO_URL)

    def testCron(self):
        with open('/home/hyfgreg/updateData/test.txt','a',encoding='utf-8') as f:
            for item in self._data['AreaCodeList'][0]:
                f.write(json.dumps(item))

    def setAreaCodeList(self):
        self._data['AreaCodeList'][0] = self.parseData(self.getAreaCodeList())

    def getAreaCodeList(self):
        try:
            response = requests.post(urlAreaCodeList, headers=evcardHeaders)
            if response.status_code == 200:
                #print(response.text)
                return response.text
            else:
                raise RequestException
        except Exception:
            raise Exception

    def saveAreaCodeList(self):
        if not self._data['AreaCodeList'][0]:
            self.setAreaCodeList()
        myL = []

        for item in self._data['AreaCodeList'][0]:
            myL.append(item)
        self.saveData(myL,'AreaCodeList')


    def saveAreaCodeListToMongo(self):
        if not self._data['AreaCodeList'][0]:
            self.setAreaCodeList()
        today = self.getDate()
        data = {today:[]}
        for item in self._data['AreaCodeList'][0]:
            data[today].append(item)
        self.saveToDB(data,Table = 'AreaCodeList')

    def uploadAreaCodeList(self):
        if not self._data['AreaCodeList'][0]:
            self.saveAreaCodeList()
        self.uploadData('AreaCodeList')

    def setShopInfoList(self):
        self._data['ShopInfoList'][0] = self.parseData(self.getShopInfoList())

    def getShopInfoList(self):
        try:
            response = requests.post(urlShopInfoList, headers=evcardHeaders)
            if response.status_code == 200:
                return response.text
                # print(response.status_code)
            else:
                print(response.status_code)
                return response.status_code
        except RequestException:
            raise RequestException

    def getCityList(self):
        db = self._client[MONGO_DB['evcard']]['AreaCodeList']
        if not db.find_one({self.getDate(): {'$exists': True}}, {'_id': 0}):
            self.setAreaCodeList()
            self.saveAreaCodeListToMongo()
        # data = db.find_one({self.getDate():{'$exists':True}},{'_id':0})
        data = db.find_one({self.getDate(): {'$exists': True}}, {'_id': 0})
        # print(data)
        tmp = data.get(self.getDate())
        # print(tmp)
        cityList = list(set([item.get('city') for item in tmp]))
        cityListEn = []
        for item in cityList:
            nameL = py.hanzi2pinyin(item[:-1])
            if 'zhong' in nameL:
                nameL[nameL.index('zhong')] = 'chong'
            name = ''.join(nameL).capitalize()
            cityListEn.append(name)
        self.cityList = cityList
        self.cityListEN = cityListEn
        # print(cityList)
        # print(cityListEn)

    def parseShopInfoList(self):
        self.getCityList()
        # client = pymongo.MongoClient(MONGO_URL)
        # db = self._client[MONGO_DB['evcard']]['AreaCodeList' + self.getDate()] # 这里也有问题！！！
        today = self.getDate()
        db = self._client[MONGO_DB['evcard']]['AreaCodeList']
        cityDict = {key:{'network_node_evcard':[]} for key in self.cityListEN}
        dataTemp = self.parseData(self.getShopInfoList())
        # print(dataTemp)
        uid = 1
        no = []
        allDict = {'network_node_evcard':[]}
        allCity = db.find_one({today: {'$exists': True}}, {'_id': 0})
        codeToCity = {}
        for item in allCity.get(today):
            codeToCity[item.get('code')] = item.get('city')
        # print(codeToCity)
        for item in dataTemp:
            # print(item)
            node = {
                'UID':str(uid),
                'Longitude':str(item.get('longitude')/1000000),
                'Latitude':str(item.get('latitude')/1000000),
                'n_car':str(item.get('stackCnt')),
                'name':item.get('shopName'),
                'MID':str(item.get('shopSeq')),
                'address':item.get('address')
            }
            allDict['network_node_evcard'].append(node)
            areaCode = item.get('areaCode')

            try:
                city = codeToCity.get(areaCode)

                # city = db.find({'code':areaCode}).get('city') #这个有问题！！！
                cityDict[self.cityListEN[self.cityList.index(city)]]['network_node_evcard'].append(node)
                uid += 1
            except AttributeError:
                no.append(node)
                uid += 1
        # print(cityDict)
        self.cityDict = cityDict
        self._data['ShopInfoList'][0] = allDict
        # return allDict,cityDict,no
        # return no

    def saveCityShopInfoList(self):
        if not self.cityDict:
            self.parseShopInfoList()
        # today = date.today().strftime('%Y-%m-%d')
        all = self.cityDict
        for key in all.keys():
            self.saveData(all.get(key),key)
            # with open(DATAFOLDER + 'evcard' +key+ today + '.json', 'w', encoding='utf-8') as f:
            #     f.write(json.dumps(all.get(key), ensure_ascii=False, indent=4))

    def saveCityShopInfoListToMongo(self):
        if not self.cityDict:
            self.parseShopInfoList()
        all = self.cityDict
        today = self.getDate()
        data = {today:[]}
        for key in all.keys():
            node = {key:all.get(key)}
            data[today].append(node)
        self.saveToDB(data, Table='ShopInfoList')



    def uploadCityShopInfoList(self):
        try:
            if self.cityListEN == None:
                self.saveCityShopInfoList()
            for city in self.cityListEN:
                # key = self.getFileName(fileName=city)
                # localfile = DATAFOLDER + self.getFileName(fileName=city)
                # token = q.upload_token(BUCKET_NAME, key, 3600)
                # ret, info = put_file(token, key, localfile)
                # print(info)
                # assert ret['key'] == key
                # assert ret['hash'] == etag(localfile)
                # print('成功上传文档{}至{}'.format(localfile, BUCKET_NAME))
                self.uploadData(city)
        except Exception:
            pass

    def setVehicleModeList(self):
        self._data['VehicleModeList'][0] = self.parseData(self.getVehicleModeList())

    def getVehicleModeList(self):
        try:
            response = requests.post(urlVehicleModeList, headers=evcardHeaders)
            if response.status_code == 200:
                return response.text
            else:
                return response.status_code
        except RequestException:
            raise RequestException

    def saveVehicleModeList(self):
        if self._data['VehicleModeList'][0] == None:
            self.setVehicleModeList()
        myL = []
        for item in self._data['VehicleModeList'][0]:
            myL.append(item)
        self.saveData(myL,'VehicleModeList')

    def saveVehicleModeListToMongo(self):
        if not self._data['VehicleModeList'][0]:
            self.setVehicleModeList()
        today = self.getDate()
        data = {today:[]}
        for item in self._data['VehicleModeList'][0]:
            data[today].append(item)
        self.saveToDB(data,Table = 'VehicleModeList')

    def uploadVehicleModeList(self):
        if not self._data['VehicleModeList'][0]:
            self.setVehicleModeList()
        self.uploadData('VehicleModeList')

    def parseData(self,text):
        try:
            data = json.loads(text)
            myD = []
            if data:
                for item in data:
                    myD.append(item)
            return myD
        except Exception:
            raise Exception

    def getFileName(self,fileName):
        today = date.today().strftime('%Y-%m-%d')
        return MONGO_DB.get('evcard')+fileName+today+'.json'

    def saveData(self,data,fileName):
        with open(DATAFOLDER+self.getFileName(fileName),'w',encoding='utf-8') as f:
            f.write(json.dumps(data,ensure_ascii=False,indent=4))
        print('保存{0}到本地成功'.format(self.getFileName(fileName)))

    def save(self):
        try:
            for k,v in self._data.items():
                print('开始保存{0}到本地'.format(k))
                v[1]()
            return True
        except Exception as e:
            raise e

    def saveToMongo(self):
        try:
            for k,v in self._data.items():
                print('开始保存'+k+'到MongoDB')
                v[2]()
            # return True
        except Exception:
            raise Exception

    def upload(self):
        try:
            for k,v in self._data.items():
                print('开始上传{0}'.format(k))
                v[3]()
            # return True
        except Exception:
            raise Exception


    def uploadData(self,filename):
        try:
            key = self.getFileName(filename)
            localfile = DATAFOLDER + self.getFileName(filename)
            token = q.upload_token(BUCKET_NAME, key, 3600)
            ret, info = put_file(token, key, localfile)
            print(info)
            assert ret['key'] == key
            assert ret['hash'] == etag(localfile)
            print('成功上传文档{}至{}'.format(localfile, BUCKET_NAME))
            return True
        except Exception as e:
            raise e

    def saveToDB(self,data,Table = None):
        # print(dbName,Table)
        if Table:
            db = self._client[MONGO_DB.get('evcard')]
            db[Table].insert_one(data)
            print('保存成功',data)
            return True
        if Table == None:
            print('请输入集合名称')
        print('保存失败')
        return False

    def getDate(self):
        return date.today().strftime('%Y-%m-%d')


if __name__ == '__main__':
    ev = Evcard()
    ev.saveVehicleModeListToMongo()

    # allDict, cityDict, no = ev.parseShopInfoList()
    # print(allDict)
    # print(cityDict)

    # print(ev.getDate())
    # ev.setAreaCodeList()
    # # ev.testPrint()
    # ev.saveAreaCodeListToMongo()
    # ev.saveCityShopInfoList()
    #print(a)
    # for key in a.keys():
    #     with open(os.getcwd()+'\\'+key+'.json','w',encoding='utf-8') as f:
    #         f.write(json.dumps(a.get(key),ensure_ascii=False,indent=4))

