from pymongo import MongoClient
import certifi

MONGO_URI = "mongodb+srv://kaurashi2507_db_user:03e9r37ivCgt8AYg@vakeelsaathi-cluster.priaxef.mongodb.net/"

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=15000
)

try:
    print(client.admin.command("ping"))
    print("MongoDB connected successfully!")
except Exception as e:
    print("Connection failed:")
    print(repr(e))