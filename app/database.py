from pymongo import mongo_client
import pymongo
from app.config import settings

client = mongo_client.MongoClient(settings.DATABASE_URL)
print('Connected to MongoDB...')

db = client[settings.MONGO_INITDB_DATABASE]
User = db.user
Project = db.project
User.create_index([("email", pymongo.ASCENDING)], unique=True)
Project.create_index([("title", pymongo.ASCENDING)], unique=True)