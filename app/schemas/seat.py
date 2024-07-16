from pydantic import BaseModel, Field


class SeatBase(BaseModel):
    row: str = Field(..., min_length=1, max_length=5)
    number: int = Field(..., gt=0)
    type: str = Field(..., min_length=3, max_length=50)
    theater_id: int


class SeatCreate(SeatBase):
    pass

class SeatUpdate(SeatBase):
    pass

class Seat(SeatBase):
    id: int
    
    class Config:
        from_attributes = True