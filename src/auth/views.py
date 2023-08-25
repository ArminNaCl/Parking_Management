from datetime import timedelta

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm


from sqlalchemy.orm import Session
from typing import Annotated

from src.auth import service, models, schemas
from src.database import engine, get_db
from src.config import ACCESS_TOKEN_EXPIRE_MINUTES, oauth2_scheme

from src.record.schemas import Record
from src.record.service import get_records_of_user

models.Base.metadata.create_all(bind=engine)  # should move to manage.py

user_api = APIRouter()
auth_api = APIRouter()


@auth_api.post("/register", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return service.create_user(db=db, user=user)


@auth_api.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = service.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect username or password",
            headers={"WWW-Authentication": "Bearer"},
        )
    access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expire
    )
    return {"access_token": access_token, "token_type": "bearer"}

@auth_api.get("/token", response_model=schemas.Token)
def logout_for_access_token(token:Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    return service.logout_user(token,db)


@user_api.get("", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = service.get_users(db, skip=skip, limit=limit)
    return users


@user_api.get("/me", response_model=schemas.User)
async def get_current_user(
    current_user: Annotated[schemas.User, Depends(service.get_current_active_user)],
    db: Session = Depends(get_db),
):
    return current_user


@user_api.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User Not Found")
    return db_user


@user_api.get("/me/cars/", response_model=list[schemas.Car])
def get_current_user_cars(
    current_user: Annotated[schemas.User, Depends(service.get_current_active_user)],
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return service.get_user_cars(db=db, user_id=current_user.id, skip=skip, limit=limit)


@user_api.post("/{user_id}/cars/", response_model=schemas.Car)
def create_car_for_user(
    admin_user: Annotated[schemas.User, Depends(service.get_current_superuser)],
    user_id: int,
    car: schemas.CarCreate,
    db: Session = Depends(get_db),
):
    return service.create_user_car(db=db, car=car, user_id=user_id)


@user_api.get("/cars/", response_model=list[schemas.Car])
def read_cars(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    cars = service.get_cars(db, skip=skip, limit=limit)
    return cars


@user_api.get("/me/records/", response_model=list[Record])
def get_current_user_records(
    current_user: Annotated[schemas.User, Depends(service.get_current_active_user)],
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return get_records_of_user(db, user_id=current_user.id, skip=skip,limit=limit)