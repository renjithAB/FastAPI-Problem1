from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URL = "mongodb://localhost:27017"
MONGODB_DATABASE = "mydatabase"
MONGODB_COLLECTION = "files"

# MongoDB client
client = AsyncIOMotorClient(MONGODB_URL)
db = client[MONGODB_DATABASE]
collection = db[MONGODB_COLLECTION]
