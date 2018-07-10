import pymongo
import pandas as pd
from pymongo import MongoClient
import time

client = MongoClient()
db = client.BoyStory
collection = db.TPData
data = pd.DataFrame(list(collection.find()))
print(data.head())

data['date_formatted']=pd.to_datetime(data['TIME'], format='%m月%d日 %H:%M', errors='ignore')
print(data.head())
print(data.tail())