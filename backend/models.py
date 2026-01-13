from sqlalchemy import Column, Integer, String, Float, DateTime
from geoalchemy2 import Geography
from database import Base

class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(String)
    timestamp = Column(DateTime)
    aqi = Column(Integer)
    temperature = Column(Float)
    # This stores the location as a spatial point
    location = Column(Geography(geometry_type='POINT', srid=4326))