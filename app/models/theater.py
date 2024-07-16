from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.orm import relationship

from .base_model import BaseModel

class Theater(BaseModel):
    __tablename__ = "theaters"

    name = Column(String, unique=True, index=True, nullable=False)
    location = Column(String, nullable=False)
    image = Column(String)
    is_active = Column(Boolean, default=True)
    capacity = Column(Integer, nullable=False)
    screens = Column(Integer, nullable=False, default=1)

    seats = relationship("Seat", back_populates="theater")
    shows = relationship("Show", back_populates="theater")

