from collections import OrderedDict
import pymongo
from config import *

class Parse(object):
    def __init__(self):
        self._client = pymongo.MongoClient(MONGO_URL)
        self._edbusFile =['BusSchedule','RouteList','RouteStationList']
        self._evcardFile = ['']


    def edbusParse(self):
        pass