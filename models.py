from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    region = Column(String)
    package = Column(String)
    available_balance = Column(Float, default=0.0)
    reserved_balance = Column(Float, default=0.0)

class SubRegionEngine(Base):
    __tablename__ = 'sub_region_engines'
    id = Column(Integer, primary_key=True)
    region = Column(String)

class AIEarnings(Base):
    __tablename__ = 'ai_earnings'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    region = Column(String)
    earnings = Column(Float)
