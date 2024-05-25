# app/database.py
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("Your MongoDb URL")
db = client.test
collection = db.items
