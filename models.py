from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name: str
    email: str
    device_id: Optional[str] = None

class EnergyData(BaseModel):
    device_id: str
    voltage: float
    current: float
    power: float
    energy: float
