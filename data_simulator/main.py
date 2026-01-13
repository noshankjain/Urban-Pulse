import time
import json
import random
import datetime
import paho.mqtt.client as mqtt

# --------------------------------------------------------------------------
# CONFIGURATION
# --------------------------------------------------------------------------
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "urban-pulse/sensors"
MQTT_USERNAME = "user"
MQTT_PASSWORD = "password"

# A list of 30 Major World Cities
WORLD_CITIES = {
    "London": (51.5074, -0.1278), "New York": (40.7128, -74.0060), 
    "Tokyo": (35.6762, 139.6503), "Mumbai": (19.0760, 72.8777),
    "Hyderabad": (17.3850, 78.4867), "Paris": (48.8566, 2.3522),
    "Berlin": (52.5200, 13.4050), "Sydney": (-33.8688, 151.2093),
    "Dubai": (25.2048, 55.2708), "Singapore": (1.3521, 103.8198),
    "Los Angeles": (34.0522, -118.2437), "Rio de Janeiro": (-22.9068, -43.1729),
    "Moscow": (55.7558, 37.6173), "Beijing": (39.9042, 116.4074),
    "Cairo": (30.0444, 31.2357), "Mexico City": (19.4326, -99.1332),
    "Toronto": (43.6510, -79.3470), "Bangkok": (13.7563, 100.5018),
    "Istanbul": (41.0082, 28.9784), "Seoul": (37.5665, 126.9780),
    "Rome": (41.9028, 12.4964), "Madrid": (40.4168, -3.7038),
    "Chicago": (41.8781, -87.6298), "San Francisco": (37.7749, -122.4194),
    "Lagos": (6.5244, 3.3792), "Johannesburg": (-26.2041, 28.0473),
    "Buenos Aires": (-34.6037, -58.3816), "Jakarta": (-6.2088, 106.8456),
    "Delhi": (28.6139, 77.2090), "Shanghai": (31.2304, 121.4737)
}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT Broker!")
    else:
        print(f"❌ Connection Failed: {rc}")

def generate_reading(city_name, coords):
    """Generates sensor data for a specific city."""
    base_lat, base_lon = coords
    
    # Jitter the location slightly so multiple sensors in one city don't overlap
    lat_jitter = random.uniform(-0.02, 0.02)
    lon_jitter = random.uniform(-0.02, 0.02)
    
    return {
        "sensor_id": f"sensor-{city_name}", # e.g., sensor-London
        "timestamp": datetime.datetime.now().isoformat(),
        "aqi": random.randint(30, 300), # 300 is hazardous!
        "temperature": round(random.uniform(-5.0, 45.0), 2),
        "latitude": round(base_lat + lat_jitter, 6),
        "longitude": round(base_lon + lon_jitter, 6),
        "city_tag": city_name # Helper field for debug
    }

def main():
    client = mqtt.Client()
    if MQTT_USERNAME and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    
    client.on_connect = on_connect
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return

    print("🌍 Starting Global Simulation (30 Cities)...")
    
    try:
        while True:
            # Pick 5 random cities to update every cycle (to avoid flooding)
            target_cities = random.sample(list(WORLD_CITIES.items()), 5)
            
            for city, coords in target_cities:
                payload = generate_reading(city, coords)
                client.publish(MQTT_TOPIC, json.dumps(payload))
                print(f"📡 Sent update for {city}")
            
            time.sleep(1) # Wait 1 second before next batch

    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()
        print("\n🛑 Simulation Stopped.")

if __name__ == "__main__":
    main()