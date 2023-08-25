from pydantic import BaseModel


class CarBase(BaseModel):
    plate_number: str
    brand: str | None
    model: str | None
    color: str | None


class UserBase(BaseModel):
    email: str
    username: str


class CarCreate(CarBase):
    pass


class Car(CarBase):
    id: int
    owner_id: int
    owner : UserBase | None = None

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


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
