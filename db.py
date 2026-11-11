from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase

DB_URL = 'mysql+pymysql://root:dipu@localhost/test'
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)
print("Database connected...")

class Base(DeclarativeBase):
    pass
