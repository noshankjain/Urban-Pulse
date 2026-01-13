import random
import uuid
from datetime import datetime

# Lat/Lon bounds for "Central London"
LAT_MIN, LAT_MAX = 51.48, 51.52
LON_MIN, LON_MAX = -0.15, -0.05

def generate_sensor_data():
    """Generates a single random sensor reading."""
    return {
        "sensor_id": f"sensor-{random.randint(1, 10)}", # Simulating 10 fixed sensors
        "timestamp": datetime.now().isoformat(),
        "aqi": random.randint(20, 180),  # 20=Good, 180=Hazardous
        "temperature": round(random.uniform(10.0, 30.0), 2),
        "latitude": round(random.uniform(LAT_MIN, LAT_MAX), 6),
        "longitude": round(random.uniform(LON_MIN, LON_MAX), 6)
    }