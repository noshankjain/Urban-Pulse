import os
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ---------------------------------------------------------
# DATABASE CONFIGURATION
# ---------------------------------------------------------
# Logic: If we are in Docker, use the environment variable. 
# If not (running locally), default to localhost.
DEFAULT_DB_URL = "postgresql://admin:password123@127.0.0.1:5432/urban_pulse_db"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="UrbanPulse API")

@app.get("/")
def read_root():
    return {"message": "UrbanPulse API is running 🟢"}

@app.get("/api/v1/latest")
def get_latest_readings(db: Session = Depends(get_db)):
    """Fetch the latest 50 readings."""
    
    # Check if table exists first to avoid crash on empty DB
    try:
        # Fetching city_tag along with other data
        query = text("""
            SELECT sensor_id, city_tag, aqi, temperature, latitude, longitude
            FROM sensor_readings
            ORDER BY timestamp DESC
            LIMIT 50;
        """)
        result = db.execute(query).fetchall()
    except Exception as e:
        print(f"Database Error: {e}")
        return []
    
    readings = []
    for row in result:
        readings.append({
            "sensor_id": row.sensor_id,
            "city": row.city_tag,
            "aqi": row.aqi,
            "temperature": row.temperature,
            "latitude": row.latitude,
            "longitude": row.longitude
        })
    return readings