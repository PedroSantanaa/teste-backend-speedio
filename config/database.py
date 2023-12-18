from pymongo.mongo_client import MongoClient

uri = "mongodb://172.17.0.2:27017"

# Create a new client and connect to the server
client = MongoClient(uri)
db=client.siteScrap
collection_name = db["site_infos"]


