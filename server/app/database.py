from pymongo import MongoClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

client = MongoClient(MONGO_URL)
db = client["papervault"]
users_collection = db["users"]

# Create unique index on email
users_collection.create_index("email", unique=True)