from datetime import datetime

from typing import Literal

from sqlalchemy.orm import Session

from src.record import schemas, models
from src.car.models import Car


def get_records(
    db: Session,
    user_id: int = None,
    car_id: int = None,
    from_date: str = None,
    to_date: str = None,
    record_type: Literal["Open", "Close", "All"] = "All",
    skip: int = 0,
    limit: int = 100,
):
    if car_id:
        queryset = db.query(models.Record).filter(models.Record.car_id == car_id)
    elif user_id:
        queryset = db.query(models.Record).join(Car).filter(Car.owner_id == user_id)
    else:
        queryset = db.query(models.Record)
    if from_date:
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        queryset = queryset.filter(models.Record.enter_time >= from_date)
    if to_date:
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
        queryset = queryset.filter(models.Record.enter_time <= to_date)
    if record_type:
        print(record_type)
        if record_type == "Open":
            queryset = queryset.filter(models.Record.exit_time == None)
        elif record_type == "Close":
            queryset = queryset.filter(models.Record.exit_time != None)
    return queryset.offset(skip).limit(limit).all()


def get_record_by_id(db: Session, record_id: int):
    return db.query(models.Record).filter(models.Record.id == record_id).first()


def get_records_of_car(db: Session, car_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Record)
        .filter(models.Record.car_id == car_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_records_of_user(
    db: Session,
    user_id: int,
    car_id: int = None,
    from_date: str = None,
    to_date: str = None,
    record_type: Literal["Open", "Close", "All"] = "All",
    skip: int = 0,
    limit: int = 100,
):
    if car_id:
        queryset = db.query(models.Record).filter(models.Record.car_id == car_id)
    else:
        queryset = db.query(models.Record).join(Car).filter(Car.owner_id == user_id)
    if from_date:
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        queryset = queryset.filter(models.Record.enter_time >= from_date)
    if to_date:
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
        queryset = queryset.filter(models.Record.enter_time <= to_date)
    if record_type:
        print(record_type)
        if record_type == "Open":
            queryset = queryset.filter(models.Record.exit_time == None)
        elif record_type == "Close":
            queryset = queryset.filter(models.Record.exit_time != None)
    return queryset.offset(skip).limit(limit).all()


def get_open_records(db: Session, skip: int, limit: int):
    return (
        db.query(models.Record)
        .filter(models.Record.exit_time == None)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_open_record(db: Session, car_id: int):
    return (
        db.query(models.Record)
        .filter(models.Record.car_id == car_id, models.Record.exit_time == None)
        .first()
    )


def create_record(db: Session, record: schemas.RecordCreate):
    db_record = models.Record(**record)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def update_record(db: Session, record_id: int, record: schemas.Record):
    db_record = db.query(models.Record).filter(models.Record.id == record_id)
    db_record.exit_time = record.exit_time
    db.commit()
    db.refresh(db_record)
    return db_record
