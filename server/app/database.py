from pymongo import MongoClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

client = MongoClient(MONGO_URL)
db = client["papervault"]
users_collection = db["users"]
chats_collection = db["chats"]

# Create unique index on email
users_collection.create_index("email", unique=True)

# Create indexes for chats
chats_collection.create_index("chat_id", unique=True)
chats_collection.create_index("user_id")
chats_collection.create_index("created_at")