from pydantic import BaseModel

from src.auth.schemas import UserBase
from typing import Union


class CarBase(BaseModel):
    plate_number: str
    brand: Union[str , None]
    model: Union[str , None]
    color: Union[str , None]


class CarCreate(CarBase):
    pass


class Car(CarBase):
    id: int
    owner_id: int
    owner: Union[UserBase , None] = None

    class Config:
        orm_mode = True
