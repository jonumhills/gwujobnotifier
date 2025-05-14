import os
import pymongo

MONGODB_URI = os.getenv('MONGO_URI')
client = pymongo.MongoClient(MONGODB_URI)
db = client.get_database("jobs")  # Example database
for i in db.listings.find():
    print(i)
