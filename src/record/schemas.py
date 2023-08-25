import datetime

from pydantic import BaseModel

from src.auth.schemas import User, Car 

class RecordBase(BaseModel):
    car_id : int
    
    class Config:
        orm_mode = True
        
        
class RecordCreate(RecordBase):
    enter_time : datetime.datetime

        
class Record(RecordCreate):
    id: int
    exit_time : datetime.datetime | None = None
    car : Car 

    