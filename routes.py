from fastapi import APIRouter
from datetime import datetime
from pydantic import BaseModel
from database import energy_collection  # Import your MongoDB collection

router = APIRouter()

# Pydantic model as per STEP 5
class EnergyData(BaseModel):
    voltage: float
    current: float
    power: float
    relay: str
    overload: bool

# 🔥 STEP 5: NEW endpoint to save to MongoDB (replaces previous POST)
@router.post("/energy/update")
def update_energy(data: EnergyData):
    record = data.dict()
    record["timestamp"] = datetime.utcnow()
    energy_collection.insert_one(record)
    return {"message": "Energy data saved"}

# 🔥 Keep existing GET endpoint for compatibility
@router.get("/energy/latest")
def get_latest_energy():
    # Get latest record from MongoDB
    latest = energy_collection.find_one(sort=[("timestamp", -1)])
    if not latest:
        return {"voltage": 0, "current": 0, "power": 0, "relay": "off", "overload": False}
    
    # Convert ObjectId to string and remove _id for clean response
    latest.pop("_id", None)
    return latest

# Optional: Keep old endpoint for backward compatibility
@router.post("/energy") 
def receive_energy(data: dict):
    # Convert dict to EnergyData format for MongoDB
    energy_record = {
        "voltage": data.get("voltage", 0),
        "current": data.get("current", 0),
        "power": data.get("power", 0),
        "relay": data.get("relay", "off"),
        "overload": data.get("overload", False)
    }
    energy_record["timestamp"] = datetime.utcnow()
    energy_collection.insert_one(energy_record)
    return {"message": "Energy data received"}
