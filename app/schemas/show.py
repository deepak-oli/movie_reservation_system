from datetime import date, time

from pydantic import BaseModel


class ShowBase(BaseModel):
    movie_id: int
    theater_id: int
    start_time: time
    end_time: time
    date: date
    price: float
    # is_active: bool

class ShowCreate(ShowBase):
    pass

class ShowUpdate(ShowBase):
    pass

class Show(ShowBase):
    id: int
    class Config:
        from_attributes = True