from pydantic import BaseModel


class CarBase(BaseModel):
    plate_number: str
    brand: str
    model: str
    color: str
    

class UserBase(BaseModel):
    email: str
    username: str | None


class CarCreate(CarBase):
    pass

class Car(CarBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
        
class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    cars: list[Car] = []

    class Config:
        orm_mode = True


