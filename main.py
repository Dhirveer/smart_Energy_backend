from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from routes import router  # Keep your existing routes

app = FastAPI()

# Global relay state (simulated)
relay_state = {"state": "OFF"}

# 🔹 COST CONFIGURATION
COST_PER_UNIT = 6.0  # ₹ per kWh

class RelayCommand(BaseModel):
    status: int  # 1 for ON, 0 for OFF (matches your frontend)

# Global energy data (updated by ESP32)
voltage = 0.0
current = 0.0
power = 0.0

# 🔹 CORS MIDDLEWARE (allows frontend connections)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # allow all frontends (for now)
    allow_credentials=True,
    allow_methods=["*"],      # allow POST, GET, OPTIONS, etc.
    allow_headers=["*"],
)

# 🔹 EXISTING ROUTES
app.include_router(router)

# 🔹 HOME PAGE
@app.get("/")
def home():
    return {"status": "Smart Energy Backend Running"}

# 🔹 RELAY CONTROL (matches your frontend exactly)
@app.post("/relay")
def control_relay(cmd: RelayCommand):
    relay_state["state"] = "ON" if cmd.status == 1 else "OFF"
    print(f"📡 Backend relay command: {relay_state['state']}")
    return {"relay": relay_state["state"] == "ON"}

# 🔹 RELAY STATUS (for ESP32 polling)
@app.get("/relay")
def get_relay_state():
    return relay_state

# 🔹 ENERGY DATA ENDPOINT (ESP32 POSTs here)
@app.post("/energy/update")
async def update_energy_data(energy_data: dict):
    global voltage, current, power
    voltage = energy_data.get("voltage", 0.0)
    current = energy_data.get("current", 0.0)
    power = energy_data.get("power", 0.0)
    print(f"📡 ESP32 Data: V={voltage:.1f}, I={current:.2f}, P={power:.1f}")
    return {"status": "received"}

# 🔹 LATEST ENERGY DATA WITH COST CALCULATION (for frontend)
@app.get("/energy/latest")
def latest():
    global voltage, current, power
    # Calculate cost per second (power in Watts * time in hours * cost per kWh)
    energy_kwh = power * (1/3600)  # Convert Watts to kWh for 1 second
    cost = energy_kwh * COST_PER_UNIT
    return {
        "voltage": round(voltage, 1),
        "current": round(current, 2),
        "power": round(power, 1),
        "cost": round(cost, 2),
        "relay": relay_state["state"]
    }
