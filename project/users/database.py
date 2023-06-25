from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from pymongo import MongoClient
load_dotenv()
db=os.getenv("DB_NAME_1")
DATABASE_URL = f"postgresql://postgres:postgres@localhost/{db}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
def initialize_database():
    Base.metadata.create_all(bind=engine)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

client = MongoClient("mongodb://localhost:27017/")
mongo_db=os.getenv("mongo_db")
mongo_collection=os.getenv("mongo_db")
mongo_db = client["mongo_db"] 
collection = mongo_db["mongo_collection"] 
