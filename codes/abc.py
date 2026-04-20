from pymongo import MongoClient

uri = "mongodb+srv://ahnafkhan414_db_user:nrq5G4bq75YxQMpk@cluster0.k3zfgbs.mongodb.net/?appName=Cluster0"

client = MongoClient(uri)

# test connection
try:
    client.admin.command('ping')
    print("✅ Connected to MongoDB Atlas!")
except Exception as e:
    print("❌ Connection failed:", e)