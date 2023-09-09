from pydantic import BaseModel

from src.auth.schemas import UserBase


class CarBase(BaseModel):
    plate_number: str
    brand: str | None
    model: str | None
    color: str | None


class CarCreate(CarBase):
    pass


class Car(CarBase):
    id: int
    owner_id: int
    owner: UserBase | None = None

    class Config:
        orm_mode = True
