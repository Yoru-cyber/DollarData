from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine, Column, Integer, String, REAL


class Base(DeclarativeBase):
    __tablename__ = "HistoricalDollar"
    id = Column(Integer, primary_key=True)
    date = Column(String)
    currency = Column(String)
    buybid = Column(REAL)
