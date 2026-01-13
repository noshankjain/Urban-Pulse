from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ------------------------------------------------------------------
# DATABASE CONFIGURATION
# ------------------------------------------------------------------
# We use 127.0.0.1 instead of localhost to avoid IPv6 issues
# User: admin
# Password: password123
# Port: 5433 (mapped from Docker)
# DB Name: urban_pulse_db
# ------------------------------------------------------------------
DATABASE_URL = "postgresql://admin:password123@127.0.0.1:5433/urban_pulse_db"

engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models
Base = declarative_base()

def get_db():
    """Dependency to get a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()