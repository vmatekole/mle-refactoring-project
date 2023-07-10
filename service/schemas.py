from typing import Optional

from pydantic import BaseModel, Field


class BaseHouseModel(BaseModel):
    date: str
    price: float
    bedrooms: int = Field(..., lt=33)
    bathrooms: float
    sqft_living: int
    sqft_lot: int
    floors: float
    waterfront: Optional[float]
    view: float
    condition: int
    grade: int
    sqft_above: int
    sqft_basement: float
    yr_built: int
    yr_renovated: float
    zipcode: int
    lat: float
    long: float
    sqft_living15: int
    sqft_lot15: int


class HouseModel(BaseHouseModel):
    id: int

    class Config:
        orm_mode = True


class HouseModelUpdate(BaseHouseModel):

    class Config:
        orm_mode = True
