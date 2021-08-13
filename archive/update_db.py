import pymongo
import json
from os import listdir
from src.database import REMOTE
import pandas as pd

files = listdir("./archive/")
client = pymongo.MongoClient(REMOTE)
db = client["bcn_dataset"]
def create_db(files):
    print(files)
    for file in files:
        coll_name = file.split(".")[0]
        if db[coll_name]:
            pass
        else:
            db.createCollection(coll_name)
        clean_data(file)
        
        
def clean_data(file):
    df = pd.read_csv("./archive/"+file)
    try:
        ages = ["05-09" if age == '5-9' else "04-05" if age == '0-4' else age for age in list(df["Age"])]
        df["Age"] = ages
    except:
        pass
    print(f'cleaning {file}')
    upload_data(file,df)

def upload_data(file,df):
    collection = db[file.split(".")[0]]
    print(f'cleaning {file}')
    collection.delete_many({})
    print(f'uploading {file}')
    col_from_df = json.loads(df.T.to_json()).values()
    collection.insert_many(col_from_df)
    
create_db(files)