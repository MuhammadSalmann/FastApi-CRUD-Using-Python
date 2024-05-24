# app/database.py
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb+srv://210920:210920@cluster1.szirki2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1")
db = client.test
collection = db.items
