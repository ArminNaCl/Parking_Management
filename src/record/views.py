import datetime
import os

from fastapi import Depends, APIRouter, HTTPException, File, UploadFile

from sqlalchemy.orm import Session
from PIL import Image

from typing import Literal

from src.database import engine, get_db
from src.record import schemas, models, service
from src.auth.service import get_car_by_plate_number
from src.record.helper import image_to_str


models.Base.metadata.create_all(bind=engine)  # should move to manage.py


record_api = APIRouter()


@record_api.post("/records/", response_model=schemas.Record)
def create_record(plate_number: str, db: Session = Depends(get_db)):
    car = get_car_by_plate_number(db=db, plate_number=plate_number)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    record = {"car_id": car.id, "enter_time": datetime.datetime.now()}
    return service.create_record(db, record)


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


@record_api.get("/records/", response_model=list[schemas.Record])
def get_records(
    db: Session = Depends(get_db),
    from_date: str = None,
    to_date: str = None,
    record_type: Literal["Open", "Close", "All"] = "All",
    car_id: int = None,
    user_id: int = None,
    limit: int = 100,
    skip: int = 0,
):
    return service.get_records(
        db,
        user_id=user_id,
        car_id=car_id,
        from_date=from_date,
        to_date=to_date,
        record_type=record_type,
        limit=limit,
        skip=skip,
    )


@record_api.post("/records/add/")
async def create_record_with_plate(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    try:
        image_path = f"temp_{file.filename}"
        with open(image_path, "wb") as f:
            f.write(file.file.read())

        image = Image.open(image_path)
        plate_number = image_to_str(image)

        car = get_car_by_plate_number(db=db, plate_number=plate_number)
        if not car:
            raise HTTPException(status_code=404, detail="Car not found")

        record = {"car_id": car.id, "enter_time": datetime.datetime.now()}
        record = service.create_record(db, record)

        image.close()
        os.remove(image_path)

        return {"message": "Record created successfully", "record_id": record.id}
    except Exception as e:
        return {"message": "Error creating record", "error": str(e)}
