from pydantic import BaseModel
from .actor import Actor
class MovieBase(BaseModel):
    name: str
    description: str
    posters: list[str] = []
    genres: list[str]
    release_date: str
    duration: float

class MovieCreate(MovieBase):
    actors: list[int]

class Movie(MovieBase):
    id: int
    # actors:  Actor

    class Config:
        from_attributes = True