from pymongo import MongoClient
import redis
import os

# -------------------------
# MongoDB Configuration
# -------------------------

# If running in Docker → use service name "mongo"
# If running locally → fallback to localhost
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017/travel_db"
)

mongo_client = MongoClient(MONGO_URI)
db = mongo_client["travel_db"]

print("MongoDB Connected ✅")


# -------------------------
# Redis Configuration
# -------------------------

# If running in Docker → REDIS_HOST will be "redis"
# If running locally → fallback to localhost
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

# Test Redis connection
try:
    redis_client.ping()
    print("Redis Connected ✅")
except redis.exceptions.ConnectionError:
    print("Redis Connection Failed ❌")