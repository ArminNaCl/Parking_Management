
from sqlalchemy.orm import Session
from src.database import get_db

from src.record import schemas, models


def get_records(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Record).offset(skip).limit(limit).all()

def get_record_by_id(db: Session, record_id: int):
    return db.query(models.Record).filter(models.Record.id == record_id).first()

def get_records_of_car(db: Session, car_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Record).filter(models.Record.car_id == car_id).offset(skip).limit(limit).all()

def get_records_of_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Record).filter(models.Record.car.user_id == user_id).offset(skip).limit(limit).all()

def get_open_records(db:Session, skip:int, limit:int):
    return db.query(models.Record).filter(models.Record.exit_time == None).offset(skip).limit(limit).all()

def get_open_record(db:Session, car_id:int ):
        return db.query(models.Record).filter(models.Record.car_id == car_id, models.Record.exit_time == None).first()


def create_record(db:Session, record:schemas.RecordCreate):
    db_record = models.Record(**record)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def update_record(db:Session, record_id:int, record:schemas.Record):
    db_record = db.query(models.Record).filter(models.Record.id == record_id)
    db_record.exit_time=record.exit_time
    db.commit()
    db.refresh(db_record)
    return db_record