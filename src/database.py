from config import DBURL
from pymongo import MongoClient
import sys
sys.path.append("/Users/angel/Documents/MidBootcamp/mbc_core/")

client = MongoClient(DBURL)
db = client.get_database('bcn_dataset')

population = db.population
unemployment = db.unemployment