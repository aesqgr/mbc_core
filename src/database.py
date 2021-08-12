from config import DBURL
from pymongo import MongoClient
import sys
import os
import dotenv
dotenv.load_dotenv()

LOCAL = "mongodb://localhost:27017/"
ATLAS_PASS = os.getenv("ATLAS_PASS")

sys.path.append("/Users/angel/Documents/MidBootcamp/mbc_core/")
REMOTE = f"mongodb+srv://aesqgr:{ATLAS_PASS}@mbc-cluster.umftg.mongodb.net/"

client = MongoClient(REMOTE)
db = client.get_database('bcn_dataset')

population = db['population']