import json
import pymongo
import requests
from datetime import date
from requests.exceptions import RequestException

from config import *


class Weather(object):
    def __init__(self,city=None):
        self._city = city
        self._cityPY = None
        self._cityFileName = None
        self._client = self.setClient()
        self._weather = None
        self._check = {date.today():False}
        #self._cityid = None


    def setClient(self):
        return pymongo.MongoClient(MONGO_URL,connect=False)

    def setPY(self):
        self._cityPY = CITY.get(self._city)

    def setCityFileName(self):
        today = date.today().strftime('%Y-%m-%d')
        self.setPY()
        self._cityFileName = 'weather'+self._cityPY+today+'.json'

    def setCityWeather(self):
        url = host+path_get_weather+'city='+self._city
        #print('访问API: ', url)
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                #return response.text
                text = response.text
                weather = self.parseCityWeather(text)
                self._weather = weather
            return None
        except RequestException:
            print('请求出错, %s'%(response.status_code))
            return None

    def getCityWeather(self):
        return self._weather

    def parseCityWeather(self,text):
        if text:
            try:
                data = json.loads(text)
                if data and 'result' in data.keys():
                    result = data.get('result')
                    return result
            except Exception:
                print('解析城市天气失败！')
                return None

    def saveToMongo(self):
        if self._weather:
            db = self._client[MONGO_DB.get('天气')]
            self.setPY()
            if db[self._cityPY].insert(self._weather):
                print('成功保存到Mongo')

    def save(self):
        try:
            if self._weather == None:
                self.setCityWeather()
            self.setCityFileName()
            with open(DATAFOLDER+self._cityFileName, 'w', encoding='utf-8') as f:
                f.write(json.dumps(self._weather, ensure_ascii=False, indent=4))
                #f.write('\r')
            print('保存成功 ', self._cityFileName)
            today = date.today()
            self._check[today] = True
            return True
        except Exception as e:
            raise e

    def upload(self):
        try:
            if not self._check[date.today()]:
                #print(self._check[date.today()])
                self.save()
            else:
                print('今日已经上传{}'.format(self._cityFileName))
                return True
            key = self._cityFileName
            localfile = DATAFOLDER+self._cityFileName
            token = q.upload_token(BUCKET_NAME, key, 3600)
            ret, info = put_file(token, key, localfile)
            print(info)
            assert ret['key'] == key
            assert ret['hash'] == etag(localfile)
            print('成功上传文档{}至{}'.format(localfile, BUCKET_NAME))
            return True
        except Exception as e:
            raise e
