from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from .base_model import BaseModel

class Ticket(BaseModel):
    __tablename__ = "tickets"

    show_id = Column(Integer, ForeignKey("shows.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False)
    price = Column(Integer, nullable=False)
    is_paid = Column(Boolean, nullable=False, default=False)
    is_valid = Column(Boolean, nullable=False, default=True)

    seat = relationship("Seat", back_populates="tickets")
    # payments = relationship("Payment", back_populates="ticket")