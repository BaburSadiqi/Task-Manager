from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    DATABASE_URL = "postgresql://postgres:0786211141@localhost:5432/test"
    print("Warning: DATABASE_URL not found in env file using hardcoded postgres URL")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)


# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create a base class for declarative models
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

