from pydantic import BaseModel
from datetime import datetime

class ReadingBase(BaseModel):
    sensor_id: str
    timestamp: datetime
    aqi: int
    temperature: float
    latitude: float
    longitude: float

    class Config:
        from_attributes = True