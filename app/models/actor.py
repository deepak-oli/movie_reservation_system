from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError
from sqlalchemy.event import listen

from .base_model import BaseModel
from .movie import MovieActor

class Actor(BaseModel):
    __tablename__ = "actors"

    name = Column(String, nullable=False)
    image = Column(String)

    movies = relationship("Movie", secondary="movie_actors", back_populates="actors")



def prevent_actor_deletion(mapper, connection, target):
    if target.movies:
        raise IntegrityError(f"Cannot delete actor {target.name} because it is associated with movies.")

listen(Actor, 'before_delete', prevent_actor_deletion)
