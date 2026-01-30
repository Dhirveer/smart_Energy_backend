from pymongo import MongoClient

# MongoDB connection
MONGO_URL = "mongodb://localhost:27017"

client = MongoClient(MONGO_URL)

# Database name
db = client["smart_energy"]

# Collection names
energy_collection = db["energy_logs"]  # Added for energy data
user_collection = db["users"]
