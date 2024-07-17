from typing import List, Optional
from pydantic import BaseModel

from app.schemas.seat import Seat
from app.schemas.show import Show


class TicketBase(BaseModel):
    show_id: int
    seat_id: int
    price: int
    is_paid: Optional[bool] = False
    is_valid: bool


class TicketCreate(TicketBase):
    pass

class TicketUpdate(TicketBase):
    pass

class Ticket(TicketBase):
    id: int
    seat: Seat
    # show: Show
    user_id: int

    class Config:
        from_attributes = True