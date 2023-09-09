from fastapi import Depends, APIRouter

from sqlalchemy.orm import Session
from typing import Annotated, Literal

from src.database import engine, get_db
from src.auth import (
    models as auth_models,
    schemas as auth_schemas,
    service as auth_service,
)
from src.record import models as record_models, schemas as record_schemas
from src.car import schemas as car_schemas, service as car_service


auth_models.Base.metadata.create_all(bind=engine)  # should move to manage.py
record_models.Base.metadata.create_all(bind=engine)  # should move to manage.py


app_router = APIRouter()


@app_router.get("/me/", response_model=auth_schemas.User)
async def get_current_user(
    current_user: Annotated[
        auth_schemas.User, Depends(auth_service.get_current_active_user)
    ]
):
    return current_user


@app_router.get("/me/cars/", response_model=list[car_schemas.Car])
def get_current_user_cars(
    current_user: Annotated[
        auth_schemas.User, Depends(auth_service.get_current_active_user)
    ],
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return car_service.get_user_cars(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )


@app_router.get("/me/records/", response_model=list[record_schemas.Record])
def get_current_user_records(
    current_user: Annotated[
        auth_schemas.User, Depends(auth_service.get_current_active_user)
    ],
    skip: int = 0,
    limit: int = 100,
    from_date: str = None,
    to_date: str = None,
    record_type: Literal["Open", "Close", "All"] = "All",
    car_id: int = None,
    db: Session = Depends(get_db),
):
    return auth_service.get_records_of_user(
        db,
        user_id=current_user.id,
        from_date=from_date,
        to_date=to_date,
        record_type=record_type,
        skip=skip,
        limit=limit,
        car_id=car_id,
    )
