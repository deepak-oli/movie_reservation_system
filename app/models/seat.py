from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base_model import BaseModel



class Seat(BaseModel):
    __tablename__ = "seats"

    row = Column(String, nullable=False)
    number = Column(Integer, nullable=False)
    type = Column(String, nullable=False)
    theater_id = Column(Integer, ForeignKey("theaters.id"), nullable=False)

    theater = relationship("Theater", back_populates="seats")