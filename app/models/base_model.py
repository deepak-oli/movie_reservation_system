from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from app.config.db import Base


class BaseModel(Base):
    __abstract__ = True  # Prevent instantiation of this class directly

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)