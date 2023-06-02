import hashlib

from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Boolean
import sqlite3

# Database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./tests.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def create_database():
    conn = sqlite3.connect(SQLALCHEMY_DATABASE_URL[10:])
    cursor = conn.cursor()
    conn.commit()
    conn.close()


# Database models
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)


# API endpoints
# Create database and tables if they do not exist
create_database()
Base.metadata.create_all(bind=engine)
