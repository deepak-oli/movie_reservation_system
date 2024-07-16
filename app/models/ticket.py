from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .base_model import BaseModel

class Ticket(BaseModel):
    __tablename__ = "tickets"

    showtime_id = Column(Integer, ForeignKey("shows.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False)
    price = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)

    show = relationship("Show", back_populates="tickets")
    user = relationship("User", back_populates="tickets")
    seat = relationship("Seat", back_populates="tickets")
    payments = relationship("Payment", back_populates="ticket")