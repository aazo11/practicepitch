import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Environment-based database configuration
def get_database_url():
    env = os.getenv("ENVIRONMENT", "local")
    if env == "production":
        # Production PostgreSQL
        return os.getenv(
            "DATABASE_URL", 
            "postgresql://username:password@localhost:5432/practicepitch_prod"
        )
    else:
        # Local SQLite
        return os.getenv("DATABASE_URL", "sqlite:///./local.db")

DATABASE_URL = get_database_url()

# Create engine with appropriate settings
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False, index=True)
    website = Column(String, nullable=False)
    linkedin = Column(String, nullable=False)
    pitch_deck = Column(String, nullable=False)
    github = Column(String, nullable=True)
    email = Column(String, nullable=False, index=True)
    meeting_time = Column(String, nullable=False)
    zoom_link = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending, scheduled, completed, cancelled
    crawl_data = Column(Text, nullable=True)  # JSON string of crawled data
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Dependency for getting database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 