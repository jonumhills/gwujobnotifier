
import pymongo
import certifi
import json
from bson.json_util import dumps
import os
from dotenv import load_dotenv

load_dotenv()

mongouri = os.getenv('MONGO_URI')
# Send a ping to confirm a successful connection
try:
    # Create a new client and connect to the server
    print(certifi.where())
    client = pymongo.MongoClient(mongouri, tls=True, tlsCAFile=certifi.where())
    print("Did the connection")
    print(client.list_database_names())
    db = client["jobs"]

    # Specify the collection name
    collection_name = "gwu"
    collection = db[collection_name]

    # Query the collection
    # You can use find() to get all documents or add a query filter
    # For example, to get all documents:
    documents = collection.find()

    documentsList = list(documents)
    jDFromMDB = []
    for i in documentsList:
        jDFromMDB.append(i['Job Description'])
    print(jDFromMDB)
except Exception as e:
    print(e)