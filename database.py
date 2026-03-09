from pymongo import MongoClient
import os

mongo_client = None
db = None

def init_db(app):
    global mongo_client, db
    mongo_uri = app.config.get('MONGO_URI', 'mongodb://localhost:27017/ecommerce')
    mongo_client = MongoClient(mongo_uri)
    db = mongo_client['ecommerce']
    return db

def get_db():
    return db
