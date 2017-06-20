from tool.weather import Weather
from tool.edbus import Edbus
from tool.evcard import Evcard
from config import CITY
from pinyin.pinyin import PinYin

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
    ev.save()
    ev.upload()
    ev.saveToMongo()

    # e = Edbus()
    # e.upload()
    # ev = Evcard()
    # # ev.saveAreaCodeList()
    # # ev.saveCityShopInfoList()
    # # ev.saveVehicleModeList()
    # # ev.saveAreaCodeListToMongo()
    # # ev.saveCityShopInfoListToMongo()
    # # ev.saveVehicleModeListToMongo()
    #
    # ev.uploadAreaCodeList()
    # ev.uploadCityShopInfoList()
    # ev.uploadVehicleModeList()

    # allDict, cityDict, no = ev.parseShopInfoList()
    # for key in cityDict.keys():
    #     print(key + '=' , cityDict.get(key))
    # ev.upload()
    # test = PinYin()
    # test.load_word()
    # string = "钓鱼岛是中国的"
    # print("in: %s" % string)
    # print("out: %s" % str(test.hanzi2pinyin(string=string)))
    # print("out: %s" % test.hanzi2pinyin_split(string=string, split="-"))





if __name__ == '__main__':
    main()