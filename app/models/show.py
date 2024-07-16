from sqlalchemy import Column, Integer, ForeignKey, Date, Time, Boolean
from sqlalchemy.orm import relationship

from .base_model import BaseModel

class Show(BaseModel):
    __tablename__ = "shows"

    movie_id = Column(Integer, nullable=False)
    theater_id = Column(Integer, ForeignKey("theaters.id"), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    date = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)

    theater = relationship("Theater", back_populates="shows")