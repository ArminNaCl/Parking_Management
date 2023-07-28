from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from src.auth import crud, models, schemas
from src.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine) #should move to manage.py

auth_model_api = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@auth_model_api.post("", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db:Session=Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db,user=user)


@auth_model_api.get("", response_model=list[schemas.User])
def read_users(skip: int =0 , limit:int=10, db:Session=Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users 


@auth_model_api.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db:Session= Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User Not Found")
    return db_user

@auth_model_api.post("/{user_id}/cars/", response_model=schemas.Car)
def create_car_for_user(user_id:int, car:schemas.CarCreate,db:Session=Depends(get_db)):
    return crud.create_user_car(db=db, car=car, user_id=user_id)

@auth_model_api.get("/cars/", response_model=list[schemas.Car])
def read_cars(skip:int=0, limit:int=10, db: Session=Depends(get_db)):
    cars = crud.get_items(db, skip=skip, limit=limit)
    return cars