from typing import List

import models
import schemas
from database import SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException
from models import House
from rich import print
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/houses/{house_id}", response_model=schemas.HouseModel)
def get_house(house_id: int, session: Session = Depends(get_db)):
    try:
        house = session.query(models.House).get(house_id)
        if house:
            return house
        else:
            raise HTTPException(status_code=404, detail="House not found")
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    finally:
        session.close()


@app.get("/houses", response_model=List[schemas.HouseModel])
def get_houses(session: Session = Depends(get_db)):
    try:
        houses = session.query(models.House).all()
        return houses
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    finally:
        session.close()


@app.post("/house", response_model=schemas.HouseModel)
def create_house(request: schemas.HouseModel, session: Session = Depends(get_db)):
    try:
        house = models.House(**request.dict())
        session.add(house)
        session.commit()
        session.refresh(house)
        return house
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    finally:
        session.close()


@app.post("/houses", response_model=list[schemas.HouseModel])
def create_houses(houses: List[schemas.HouseModel], session: Session = Depends(get_db)):
    try:
        for house in houses:
            house = models.House(**house.dict())
            session.add(house)            
            session.commit()
            session.refresh(house)
        return houses
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    finally:
        session.close()


@app.put("/houses/{house_id}", response_model=schemas.HouseModelUpdate)
def update_house(house_id: int, request: schemas.HouseModelUpdate, session: Session = Depends(get_db)):
    try:
        house = session.query(models.House).get(house_id)
        if house:
            for key, value in request.dict().items():
                setattr(house, key, value)
            session.commit()
            session.refresh(house)
            return house
        else:
            raise HTTPException(status_code=404, detail="House not found")
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    finally:
        session.close()


@app.delete("/houses/{house_id}", response_model=dict)
def delete_house(house_id: int, session: Session = Depends(get_db)):
    try:
        house = session.query(models.House).get(house_id)
        if house:
            session.delete(house)
            session.commit()
            return {"message": "House deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="House not found")
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    finally:
        session.close()
