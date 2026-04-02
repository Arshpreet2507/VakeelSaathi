from pymongo import MongoClient
import certifi

MONGO_URI = "mongodb+srv://kaurashi2507_db_user:03e9r37ivCgt8AYg@vakeelsaathi-cluster.priaxef.mongodb.net/"

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where()
)

db = client["vakeelSathi"]

laws_collection = db["laws"]
rights_collection = db["rights"]
checklists_collection = db["checklists"]