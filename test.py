from tool.weather import Weather
from tool.edbus import Edbus
from tool.evcard import Evcard
from config import CITY
from pinyin.pinyin import PinYin

if __name__ == '__main__':
    ev = Evcard()
    # ev.saveAreaCodeListToMongo()
    # ev.saveCityShopInfoListToMongo()
    # ev.saveVehicleModeListToMongo()