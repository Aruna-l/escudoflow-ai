from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.mongo_uri)
db = client[settings.mongo_db_name]

# Collections
users_col = db["users"]
organizations_col = db["organizations"]
notifications_col = db["notifications"]
preferences_col = db["preferences"]
api_keys_col = db["api_keys"]
password_resets_col = db["password_resets"]


async def ensure_indexes():
    """Call once on startup to create required indexes."""
    await users_col.create_index("email", unique=True)
    await organizations_col.create_index("owner_id", unique=True)
    await notifications_col.create_index("user_id", unique=True)
    await preferences_col.create_index("user_id", unique=True)
    await api_keys_col.create_index([("user_id", 1), ("name", 1)])
    await password_resets_col.create_index("token", unique=True)
    await password_resets_col.create_index("expires_at", expireAfterSeconds=0)