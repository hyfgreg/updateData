from tool.weather import Weather
from tool.edbus import Edbus
from tool.evcard import Evcard
from config import CITY

def main():
    for k,_ in CITY.items():
        w = Weather(k)
        w.save()

    # e = Edbus()
    # e.upload()
    # ev = Evcard()
    # ev.upload()




if __name__ == '__main__':
    main()