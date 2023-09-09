import datetime
import os

from fastapi import Depends, APIRouter, HTTPException, File, UploadFile

from sqlalchemy.orm import Session
from typing import Literal, Union

from src.database import engine, get_db
from src.auth import (
    models as auth_models,
    schemas as auth_schemas,
    service as auth_service,
)
from src.record import (
    models as record_models,
    schemas as record_schemas,
    service as record_service,
)
from src.car import schemas as car_schemas, service as car_service
from src.CRNN.crnn_helper import crnn_helper


auth_models.Base.metadata.create_all(bind=engine)  # should move to manage.py
record_models.Base.metadata.create_all(bind=engine)  # should move to manage.py


admin_router = APIRouter()


@admin_router.get("/users/", response_model=list[auth_schemas.UserBase])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = auth_service.get_users(db, skip=skip, limit=limit)
    return users


@admin_router.get("/users/{user_id}/", response_model=auth_schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = auth_service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User Not Found")
    return db_user


@admin_router.post("/{user_id}/cars/", response_model=car_schemas.Car)
def create_car_for_user(
    user_id: int, car: car_schemas.CarCreate, db: Session = Depends(get_db)
):
    return car_service.create_user_car(db=db, car=car, user_id=user_id)


@admin_router.get("/cars/", response_model=list[car_schemas.Car])
def read_cars(
    skip: int = 0, limit: int = 10, user_id: Union[int, None] = None, db: Session = Depends(get_db)
):
    cars = car_service.get_cars(db, skip=skip, limit=limit, user_id=user_id)
    return cars


@admin_router.get("/records/", response_model=list[record_schemas.Record])
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
    return record_service.get_records(
        db,
        user_id=user_id,
        car_id=car_id,
        from_date=from_date,
        to_date=to_date,
        record_type=record_type,
        limit=limit,
        skip=skip,
    )


@admin_router.post("/records/add/")
async def create_record_with_plate(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    try:
        image_path = f"temp_{file.filename}"
        with open(image_path, "wb") as f:
            f.write(file.file.read())

        plate_number = crnn_helper(image_path)

        car = car_service.get_car_by_plate_number(db=db, plate_number=plate_number)
        if not car:
            raise HTTPException(status_code=404, detail="Car not found")

        record = {"car_id": car.id, "enter_time": datetime.datetime.now()}
        record = record_service.create_record(db, record)

        os.remove(image_path)

        return {
            "message": "Record created successfully",
            "record_id": record_schemas.Record(record.id),
        }
    except Exception as e:
        return {"message": "Error creating record", "error": str(e)}


@admin_router.put("/records/update/", response_model=record_schemas.Record)
async def update_record_with_plate(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    try:
        image_path = f"temp_{file.filename}"
        with open(image_path, "wb") as f:
            f.write(file.file.read())

        plate_number = crnn_helper(image_path)
        car = car_service.get_car_by_plate_number(db=db, plate_number=plate_number)

        if not car:
            raise HTTPException(status_code=404, detail="Car not found")

        record = record_service.get_open_record(db=db, car_id=car.id)
        if not record:
            raise HTTPException(status_code=404, detail="Record not found")

        record.exit_time = datetime.datetime.now()
        db.commit()
        db.refresh(record)
        return record
    except Exception as e:
        return {"message": "Error Updating record", "error": str(e)}


# @record_api.post("/records/", response_model=schemas.Record)
# def create_record(plate_number: str, db: Session = Depends(get_db)):
#     car = get_car_by_plate_number(db=db, plate_number=plate_number)
#     if not car:
#         raise HTTPException(status_code=404, detail="Car not found")

#     record = {"car_id": car.id, "enter_time": datetime.datetime.now()}
#     return service.create_record(db, record)


# @record_api.put("/records/", response_model=schemas.Record)
# def update_record(plate_number: str, db: Session = Depends(get_db)):
#     car = get_car_by_plate_number(db=db, plate_number=plate_number)
#     if not car:
#         raise HTTPException(status_code=404, detail="Car not found")

#     record = service.get_open_record(db=db, car_id=car.id)
#     if not record:
#         raise HTTPException(status_code=404, detail="Record not found")

#     record.exit_time = datetime.datetime.now()
#     db.commit()
#     db.refresh(record)
#     return record
