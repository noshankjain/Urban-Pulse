-- Enable PostGIS for geospatial features
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create the table to store sensor data
CREATE TABLE IF NOT EXISTS sensor_readings (
    id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(50),
    timestamp TIMESTAMP,
    aqi INTEGER,
    temperature FLOAT,
    location GEOGRAPHY(POINT, 4326)
);