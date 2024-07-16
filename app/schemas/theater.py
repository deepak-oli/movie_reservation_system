from typing import Optional
from pydantic import BaseModel, Field

class TheaterBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    location: str = Field(..., min_length=3, max_length=100)
    image: Optional[str] = None
    capacity: int = Field(..., gt=0)
    screens: int = Field(..., gt=0)

class TheaterCreate(TheaterBase):
    pass

class TheaterUpdate(TheaterBase):
    is_active: bool = True

class Theater(TheaterBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

