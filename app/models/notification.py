import enum

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, String
from sqlalchemy.orm import relationship

from .base_model import BaseModel

class NotificationStatus(enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"

class NotificationType(enum.Enum):
    TICKET = "ticket"
    PAYMENT = "payment"
    SHOW = "show"
    INFO = "info"
    MARKETING = "marketing"

class NotificationMode(enum.Enum):
    EMAIL = "email"
    PUSH = "push"


class Notification(BaseModel):
    __tablename__ = "notifications"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String, nullable=False)
    status = Column(Enum(NotificationStatus), nullable=False)
    type = Column(Enum(NotificationType), nullable=False)
    mode = Column(Enum(NotificationMode), nullable=False)
    date = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="notifications")
    