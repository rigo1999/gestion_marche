import pymongo

def get_db_connection():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    return client["market_db"]