import enum

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship

from .base_model import BaseModel

class PaymentStatus(enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"

class PaymentMethod(enum.Enum):
    CASH = "cash"
    CARD = "card"
    ONLINE = "online"


class Payment(BaseModel):
    __tablename__ = "payments"

    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    method = Column(Enum(PaymentMethod), nullable=False)
    status = Column(Enum(PaymentStatus), nullable=False)
    date = Column(DateTime, nullable=False)

    ticket = relationship("Ticket", back_populates="payments")
    user = relationship("User", back_populates="payments")