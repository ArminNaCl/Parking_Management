from fastapi import Depends

from sqlalchemy.orm import Session
from typing import Union


from src.car import models, schemas


def get_cars(db: Session, skip: int = 0, limit: int = 10, user_id: Union[int, None]=None):
    queryset = db.query(models.Car)
    if user_id:
        queryset = queryset.filter(models.Car.owner_id == user_id)
    return queryset.offset(skip).limit(limit).all()


def get_car_by_plate_number(db: Session, plate_number: str):
    return db.query(models.Car).filter(plate_number == models.Car.plate_number).first()


def get_user_cars(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(models.Car)
        .filter(models.Car.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_user_car(db: Session, car: schemas.CarCreate, user_id: int):
    db_car = models.Car(**car.dict(), owner_id=user_id)
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


def get_or_create_user_car(
    db: Session, car: Depends(get_car_by_plate_number), plate_number: str, user_id=int
):
    create_flag = False
    if car:
        return car, create_flag
    car = create_user_car(car={"plate_number": plate_number}, user_id=user_id)
