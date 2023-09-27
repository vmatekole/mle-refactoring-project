from sqlalchemy import BigInteger, Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class House(Base):
    __tablename__ = 'houses'

    id = Column(BigInteger, primary_key=True)
    date = Column(String, nullable=True)
    price = Column(Float)
    bedrooms = Column(Integer)
    bathrooms = Column(Float)
    sqft_living = Column(Integer)
    sqft_lot = Column(Integer)
    floors = Column(Float)
    waterfront = Column(Float)
    view = Column(Float)
    condition = Column(Integer)
    grade = Column(Integer)
    sqft_above = Column(Integer)
    sqft_basement = Column(Float)
    yr_built = Column(Integer)
    yr_renovated = Column(Float)
    zipcode = Column(Integer)
    lat = Column(Float)
    long = Column(Float)
    sqft_living15 = Column(Integer)
    sqft_lot15 = Column(Integer)
