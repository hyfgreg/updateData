import os
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
import platform

MONGO_URL = 'localhost'

MONGO_DB = {
    '天气':'weather',
    '驿动':'edbus',
    'evcard':'evcard'
}

CITY = {
    '上海':'Shanghai',
    '北京':'Beijing',
    '广州':'Guangzhou'
}

###天气的配置
host = 'http://jisutianqi.market.alicloudapi.com'
path_get_city = '/weather/city'
path_get_weather = '/weather/query?'
appcode = '6a4b15325da84f5bbef0e74a39987931'
headers = {"Authorization": "APPCODE 6a4b15325da84f5bbef0e74a39987931"}


###evcard的配置
urlAreaCodeList = 'http://www.evcardchina.com/api/proxy/getAreaCodeList'
urlShopInfoList = 'http://www.evcardchina.com/api/proxy/getShopInfoList'
urlVehicleModeList = 'http://www.evcardchina.com/api/proxy/getVehicleModeList'
evcardHeaders = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }




###edbus的配置
baseTest = 'http://121.40.16.219:20010/yidong'
base = 'http://ydwl.ev-shanghai.com/yidong'
# 以下是不同的Url
urlCarDynamic = '/tj/route/getRouteCarDynamic.jhtml'  # 车辆动态信息
urlBusSchedule = '/tj/route/queryBusSchedule.jhtml'  # 巴士安排
urlRouteStationList = '/tj/route/queryRouteStationList.jhtml'  # 站点信息
urlRouteList = '/tj/route/queryRouteList.jhtml'  # 线路信息
# 以下是生成签名
key = '12Xso1XU9sd3SDJ8s0kcsxops9'



###上传的配置
if platform.platform().startswith('W'):
    DATAFOLDER = os.getcwd()+'\\data\\'
else:
    DATAFOLDER = os.getcwd() + '/data/'
BUCKET_NAME = 'yimove'
access_key = 'WxtU5PasZSCeEnuWZl_QtnlaIanDVSN7jO4s03HC'
secret_key = 'GeRvR9HYjmwaM75PilZumocBfmfnv7KboMFWVp1f'
q = Auth(access_key, secret_key)