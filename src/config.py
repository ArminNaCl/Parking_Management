from .local_config import *

from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext


#Databae
SQLALCHEMY_DATABASE_URL = LOCAL_SQLALCHEMY_DATABASE_URL


#JWT
SECRET_KEY = LOCAL_SECRET_KEY
ALGORITHM = LOCAL_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = LOCAL_ACCESS_TOKEN_EXPIRE_MINUTES






oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


