from sqlalchemy import Column, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base



class Record(Base):
    __tablename__ = "records"
    
    id = Column(Integer, primary_key=True, index=True)
    enter_time = Column(DateTime, default=func.now())
    exit_time = Column(DateTime, nullable=True)
    
    car_id = Column(Integer, ForeignKey("cars.id"))
    
    car = relationship("Car", back_populates="records")