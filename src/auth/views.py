from datetime import timedelta

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm


from sqlalchemy.orm import Session
from typing import Annotated

from src.auth import service, models, schemas
from src.database import engine, get_db
from src.config import ACCESS_TOKEN_EXPIRE_MINUTES, oauth2_scheme

models.Base.metadata.create_all(bind=engine)  # should move to manage.py

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
def logout_for_access_token(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    return service.logout_user(token, db)
