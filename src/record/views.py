import datetime

from fastapi import Depends, APIRouter, HTTPException

from sqlalchemy.orm import Session

from src.database import engine, get_db
from src.record import schemas, models, service
from src.auth.service import get_car_by_plate_number


models.Base.metadata.create_all(bind=engine)  # should move to manage.py


record_api = APIRouter()


@record_api.post("/records/", response_model=schemas.Record)
def create_record(plate_number: str, db: Session = Depends(get_db)):
    car = get_car_by_plate_number(db=db, plate_number=plate_number)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    record = {"car_id": car.id, "enter_time": datetime.datetime.now()}
    a = service.create_record(db, record)

    return a


@record_api.put("/records/", response_model=schemas.Record)
def update_record(plate_number: str, db: Session = Depends(get_db)):
    car = get_car_by_plate_number(db=db, plate_number=plate_number)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    record = service.get_open_record(db=db, car_id=car.id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    record.exit_time = datetime.datetime.now()
    db.commit()
    db.refresh(record)
    return record

    return a


@record_api.get("/records/", response_model=list[schemas.Record])
def get_records(db: Session = Depends(get_db), limit: int = 100, skip: int = 0):
    return service.get_records(db, limit=limit, skip=skip)
