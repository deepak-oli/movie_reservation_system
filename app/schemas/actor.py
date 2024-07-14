from pydantic import BaseModel
from typing import Optional

class ActorBase(BaseModel):
    name: str
    image: Optional[str] = None

class ActorCreate(ActorBase):
    pass

class Actor(ActorBase):
    id: int

    class Config:
        from_attributes = True