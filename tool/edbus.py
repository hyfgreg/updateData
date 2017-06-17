import json
import uuid
from collections import OrderedDict
from hashlib import md5
from urllib.parse import urlencode
import requests
import pymongo
import time

from datetime import date

from config import *

class Edbus(object):
    def __init__(self):
        self._data = OrderedDict(
            {
                'BusSchedule': [None, self.setBusSchedule],
                'RouteList': [None, self.setRouteList],
                'RouteStationList': [None, self.setRouteStationList]
            }
        )
        self._routeSeq = []
        #self._client = self.setClient()

    def setClient(self):
        return pymongo.MongoClient(MONGO_URL,connect=False)

    #对外接口
    def busSchedule(self):
        if self._data['BusSchedule'][0] == None:
            self.setBusSchedule()
        return self._data['BusSchedule'][0]

    def setBusSchedule(self):
        self._data['BusSchedule'][0] = self.parseData(self.getBusSchedule())

    #获取巴士排班
    def getBusSchedule(self):

        nonceStr = str(uuid.uuid4())
        timestamp = str(int(time.time()))
        scheduleDate = time.strftime('%Y-%m-%d', time.localtime(time.time()))

        signParam = 'nonceStr=' + nonceStr + '&scheduleDate=' + scheduleDate + '&timestamp=' + timestamp + '&key=' + key
        signValue = md5(signParam.encode('utf-8')).hexdigest().upper()

        # print('&scheduleDate={scheduleDate}'.format(scheduleDate=scheduleDate))
        url = baseTest + urlBusSchedule + '?' + signParam
        try:
            response = requests.post(url, data={'sign': signValue})
            if response.status_code == 200:
                # print(response.text)
                return response.text
            else:
                print('获取失败: ', response.status_code)
                return None
        except Exception as e:
            print('请求出错:', e.args)

    def setRouteStationList(self):
        self._data['RouteStationList'][0] = self.parseRouteStationList(self.getRouteStationList())

    # 获取站点信息
    def getRouteStationList(self):

        nonceStr = str(uuid.uuid4())
        timestamp = str(int(time.time()))

        self.getRouteSeq()
        for seq in self._routeSeq:
            signParam = 'nonceStr=' + nonceStr + '&routeSeq=' + seq + '&timestamp=' + timestamp + '&key=' + key
            signValue = md5(signParam.encode('utf-8')).hexdigest().upper()
            url = baseTest + urlRouteStationList + '?' + signParam
            try:
                response = requests.post(url, data={'sign': signValue})
                if response.status_code == 200:
                    # print(response.text)
                    yield response.text
                else:
                    print('获取失败: ', response.status_code)
            except Exception as e:
                print('请求出错:', e.args)

    def parseRouteStationList(self,textIter):
        try:
            routeStationList = {'network_node_edbus': []}
            uid = 1
            for text in textIter:
                data = json.loads(text)


                if data and 'data' in data.keys():
                    items = data.get('data')
                    for item in items:
                        route = {
                            'UID':uid,
                            'LineID':str(item.get('routeSeq')),
                            'lineName':item.get('routeName'),
                            'Longitude':str(item.get('longitude')),
                            'Latitude':str(item.get('latitude')),
                            'MID':str(item.get('flag')),
                            'name':str(item.get('stationName')),
                            'type':str(item.get('type'))
                        }
                        uid += 1
                        routeStationList['network_node_edbus'].append(route)
            return routeStationList
        except Exception:
            raise Exception

    def printRouteStationList(self):
        if self._data['RouteStationList'][0]:
            return self._data['RouteStationList'][0]

    def getRouteSeq(self):
        if not self._data['RouteList'][0]:
            self.setRouteList()
        routeList = self._data['RouteList'][0]['network_line_edbus']
        for item in routeList:
            self._routeSeq.append(item.get('LineID'))
        #print(self._routeSeq)

    def printRouteList(self):
        if self._data['RouteList'][0]:
            return self._data['RouteList'][0]

    #设置线路信息
    def setRouteList(self):
        self._data['RouteList'][0] = self.parseRouteList(self.getRouteList())

    #获取线路信息
    def getRouteList(self):
        nonceStr = str(uuid.uuid4())
        timestamp = str(int(time.time()))

        signParam = 'nonceStr=' + nonceStr + '&timestamp=' + timestamp + '&key=' + key
        signValue = md5(signParam.encode('utf-8')).hexdigest().upper()
        url = baseTest+urlRouteList+'?'+signParam
        try:
            response = requests.post(url,data={'sign':signValue})
            if response.status_code == 200:
                #print(response.text)
                return response.text
            else:
                print('获取失败: ',response.status_code)
        except Exception as e:
            print('请求出错:',e.args)

    def parseRouteList(self,text):
        try:
            data = json.loads(text)
            if data and 'data' in data.keys():
                items = data.get('data')
                routeList = {'network_line_edbus':[]}
                for item in items:
                    route = {
                        'LineID':str(item.get('routeSeq')),
                        'name':item.get('routeName')
                    }
                    routeList['network_line_edbus'].append(route)
                return routeList
        except Exception:
            raise Exception



    def parseData(self,text):
        try:
            data = json.loads(text)
            if data and 'data' in data.keys():
                items = data.get('data')
                for item in items:
                    yield item
        except Exception:
            raise Exception

    def getFileName(self,fileName):
        today = date.today().strftime('%Y-%m-%d')
        return MONGO_DB.get('驿动')+fileName+today+'.json'

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
            return True
        except Exception as e:
            raise e

# def save2DB(item,Table=None):
#     if Table and db[Table].insert(item):
#         print('保存到DB成功,',item)
#         return True
#     if Table==None:
#         print('请输出集合名称!')
#     return False

if __name__ == '__main__':
    e = Edbus()
    e.setRouteStationList()
    print(e.printRouteStationList())