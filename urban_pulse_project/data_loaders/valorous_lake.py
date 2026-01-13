if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
import json
import time
import paho.mqtt.client as mqtt
import pandas as pd

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
# ⚠️ CRITICAL CHANGE: Use the container name, NOT localhost
MQTT_BROKER = "urbanpulse_broker" 
MQTT_PORT = 1883
MQTT_TOPIC = "urban-pulse/sensors"
MQTT_USERNAME = "user"
MQTT_PASSWORD = "password"

# Lists to store data
data_buffer = []

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"✅ Connected to {MQTT_BROKER}!")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"❌ Connection Failed: {rc}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(f"📥 Received: {payload}")
        data_buffer.append(payload)
    except Exception as e:
        print(f"Error decoding: {e}")

@data_loader
def load_data(*args, **kwargs):
    """
    Connects to MQTT, listens for 5 seconds, and returns a DataFrame.
    """
    global data_buffer
    data_buffer = []  # Clear buffer
    
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    
    print(f"🚀 Connecting to {MQTT_BROKER}...")
    
    try:
        # Connect to the Docker container name
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        
        # Listen for 5 seconds to collect a batch of data
        time.sleep(5)
        
        client.loop_stop()
        client.disconnect()
        
        if not data_buffer:
            print("⚠️ No data received. Is the simulator running?")
            return pd.DataFrame()
            
        print(f"✅ Finished. Collected {len(data_buffer)} rows.")
        return pd.DataFrame(data_buffer)
        
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return pd.DataFrame()