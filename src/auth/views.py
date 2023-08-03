from datetime import timedelta

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm


from sqlalchemy.orm import Session
from typing import Annotated

from src.auth import service, models, schemas
from src.database import engine, get_db
from src.config import ACCESS_TOKEN_EXPIRE_MINUTES

models.Base.metadata.create_all(bind=engine)  # should move to manage.py

auth_model_api = APIRouter()


@auth_model_api.post("", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return service.create_user(db=db, user=user)


@auth_model_api.get("", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = service.get_users(db, skip=skip, limit=limit)
    return users


@auth_model_api.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:Session=Depends(get_db)):
    user = service.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "incorrect username or password",
            headers={"WWW-Authentication":"Bearer"}
        )
    access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(
        data = {"sub": user.username}, expires_delta=access_token_expire
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_model_api.get("/me", response_model=schemas.User)
async def get_current_user(
    current_user: Annotated[schemas.User, Depends(service.get_current_active_user)],
    db: Session = Depends(get_db),
):
    return current_user


@auth_model_api.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User Not Found")
    return db_user


@auth_model_api.post("/{user_id}/cars/", response_model=schemas.Car)
def create_car_for_user(
    user_id: int, car: schemas.CarCreate, db: Session = Depends(get_db)
):
    return service.create_user_car(db=db, car=car, user_id=user_id)


@auth_model_api.get("/cars/", response_model=list[schemas.Car])
def read_cars(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    cars = service.get_items(db, skip=skip, limit=limit)
    return cars
