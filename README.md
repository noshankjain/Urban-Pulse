# 🏙️ Urban Pulse – Global Real-Time IoT Sensor Network

**Urban Pulse** is an end-to-end data engineering platform for real-time environmental monitoring.  
It simulates, processes, and visualizes live IoT sensor streams from major cities around the world.

Built using **Mage AI, RabbitMQ (MQTT)**, and a **Streamlit live dashboard**, it converts raw sensor data into actionable insights, tracking **Air Quality Index (AQI)** and **Temperature** globally.

---

## 🚀 Key Features

- **Microservices Architecture**  
  Fully containerized system with decoupled Ingestion, ETL, and Visualization layers.

- **Real-Time Data Ingestion**  
  High-throughput MQTT messaging using RabbitMQ.

- **Automated ETL Pipeline**
  - 🔄 Extract: Consumes live MQTT data from RabbitMQ  
  - 🛠️ Transform: Cleans and formats geo-tagged sensor data  
  - 💾 Load: Stores historical data in PostgreSQL  

- **Live Geospatial Dashboard**  
  Interactive world map showing active sensors, city-level search, and hazardous AQI alerts.

- **Scalable Simulation**  
  Simulates 30+ concurrent IoT devices for cities like Paris, Tokyo, and New York.

---

## 🛠️ Tech Stack

| Layer        | Technology                              |
|--------------|------------------------------------------|
| Frontend     | Streamlit, Plotly Express, Geopy         |
| Backend      | Python, FastAPI (Uvicorn)                |
| ETL          | Mage AI                                  |
| Broker       | RabbitMQ (MQTT Plugin Enabled)           |
| Database     | PostgreSQL (PostGIS Ready)               |
| Deployment   | Docker & Docker Compose                  |

---

## ⚙️ Prerequisites

- Docker Desktop  
- Python 3.9+  
- Git  

---

## 📦 Installation

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/urban-pulse.git
cd urban-pulse
```

---

### 2. Start Infrastructure (Docker)

Starts Database, Broker, Mage AI, Backend, and Frontend containers.

```bash
docker-compose up -d --build
```

Wait a few minutes for services to become healthy.

---

### 3. Setup Data Simulator (Local)

```bash
python -m venv venv
.\venv\Scripts\activate   # Windows
source venv/bin/activate # Linux/Mac

pip install paho-mqtt
```

---

## ▶️ Running the System

### Terminal 1 – Docker Infrastructure
```bash
docker-compose up -d
```

### Terminal 2 – Start Simulator
```bash
python data_simulator/main.py
```

---

## 🌐 Access the Platform

| Service      | URL                         |
|-------------|------------------------------|
| Dashboard   | http://localhost:8501       |
| Mage AI     | http://localhost:6789       |
| API Docs    | http://localhost:8000/docs  |

---

## 🚦 Activate ETL Pipeline (First Run Only)

1. Open Mage UI: http://localhost:6789  
2. Open `urban_pulse_project` pipeline  
3. Click **Loader Block (MQTT)** → ▶️ Play  
4. Click **Exporter Block (Postgres)** → ▶️ Play  

---

## ⚠️ Troubleshooting

| Error                          | Fix                                                     |
|--------------------------------|----------------------------------------------------------|
| Dashboard shows Connection Refused | Wait 30s and refresh                                    |
| No Data Stream Detected        | Ensure simulator is running                              |
| `ModuleNotFoundError: paho`    | `docker exec -it urbanpulse_mage pip install paho-mqtt` |
| RabbitMQ Connection Failed     | Enable plugin: `rabbitmq-plugins enable rabbitmq_mqtt` |

---

## 🔄 Customize Simulation

Open `data_simulator/main.py`

```python
WORLD_CITIES = {
    "London": (51.5074, -0.1278),
    "Your_City": (LATITUDE, LONGITUDE),
}
```

New cities will automatically appear on the live dashboard map.
