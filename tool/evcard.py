import json
from collections import OrderedDict
import requests
import pymongo
import time
from requests.exceptions import RequestException
from datetime import date

from config import *

class Evcard(object):
    def __init__(self):
        self._data = OrderedDict(
            {
                'AreaCodeList': [None, self.setAreaCodeList],
                'ShopInfoList': [None, self.saveCityShopInfoList],
                'VehicleModeList': [None, self.setVehicleModeList]
            }
        )
        self.cityList = None
        # self._client = self.setClient()

    def setClient(self):
        return pymongo.MongoClient(MONGO_URL,connect=False)

    def testPrint(self):
        for item in self._data['ShopInfoList'][0]:
            print(item)

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


    def setShopInfoList(self):
        self._data['ShopInfoList'][0] = self.parseData(self.getShopInfoList())

    def getShopInfoList(self):
        try:
            response = requests.post(urlShopInfoList, headers=evcardHeaders)
            if response.status_code == 200:
                return response.text
            else:
                return response.status_code
        except RequestException:
            raise RequestException

    def parseShopInfoList(self):
        client = pymongo.MongoClient(MONGO_URL)
        db = client['evcard']['AreaCodeList']
        cityList = db.find().distinct('city')
        self.cityList = cityList
        cityDict = {key:{'network_node_evcard':[]} for key in cityList}
        dataTemp = self.parseData(self.getShopInfoList())
        uid = 1
        no = []
        allDict = {'network_node_evcard':[]}

        for item in dataTemp:
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
                city = db.find_one({'code':areaCode}).get('city')
                cityDict[city]['network_node_evcard'].append(node)
                uid += 1
            except AttributeError:
                no.append(node)
                uid += 1

        return allDict,cityDict,no

    def saveCityShopInfoList(self):
        self._data['ShopInfoList'][0],all,_ = self.parseShopInfoList()
        today = date.today().strftime('%Y-%m-%d')
        for key in all.keys():
            with open(DATAFOLDER + 'evcard' +key+ today + '.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(all.get(key), ensure_ascii=False, indent=4))

    def uploadCityShopInfoList(self):
        try:
            if self.cityList == None:
                self.saveCityShopInfoList()
            for city in self.cityList:
                key = self.getFileName(fileName=city)
                localfile = DATAFOLDER + self.getFileName(fileName=city)
                token = q.upload_token(BUCKET_NAME, key, 3600)
                ret, info = put_file(token, key, localfile)
                print(info)
                assert ret['key'] == key
                assert ret['hash'] == etag(localfile)
                print('成功上传文档{}至{}'.format(localfile, BUCKET_NAME))
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

    def parseData(self,text):
        try:
            data = json.loads(text)
            if data:
                for item in data:
                    yield item
        except Exception:
            raise Exception

    def getFileName(self,fileName):
        today = date.today().strftime('%Y-%m-%d')
        return MONGO_DB.get('evcard')+fileName+today+'.json'

    def save(self):
        try:
            for k,v in self._data.items():
                print(k)
                if v[0] == None:
                    v[1]()
                with open(DATAFOLDER + self.getFileName(fileName=k), 'w', encoding='utf-8') as f:
                    myL = []
                    for item in v[0]:
                        myL.append(item)
                    f.write(json.dumps(myL, ensure_ascii=False, indent=4))
                    #f.write('\r')
                print('保存成功 ', k)
            return True
        except Exception as e:
            raise e

    def upload(self):
        try:
            self.save()
            for k,v in self._data.items():
                key = self.getFileName(fileName=k)
                localfile = DATAFOLDER + self.getFileName(fileName=k)
                token = q.upload_token(BUCKET_NAME, key, 3600)
                ret, info = put_file(token, key, localfile)
                print(info)
                assert ret['key'] == key
                assert ret['hash'] == etag(localfile)
                print('成功上传文档{}至{}'.format(localfile, BUCKET_NAME))
            self.uploadCityShopInfoList()
            return True
        except Exception as e:
            raise e

if __name__ == '__main__':
    ev = Evcard()
    ev.saveCityShopInfoList()
    #print(a)
    # for key in a.keys():
    #     with open(os.getcwd()+'\\'+key+'.json','w',encoding='utf-8') as f:
    #         f.write(json.dumps(a.get(key),ensure_ascii=False,indent=4))

