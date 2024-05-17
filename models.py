# models.py
from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
Base = declarative_base()

class Jersey(Base):
    __tablename__ = 'jerseys'
    id = Column(Integer, primary_key=True, index=True)
    team = Column(String, index=True)
    league = Column(String)
    type = Column(String)
    home_away_third = Column(String)
    size = Column(String)
    number_of_jerseys = Column(Integer)
    price = Column(Float)
    customizable = Column(Boolean)
    discounted_price = Column(Float)
