from sqlalchemy import String, Column, ARRAY, Integer, ForeignKey 
from sqlalchemy.orm import relationship

from .base_model import BaseModel

class Movie(BaseModel):
    __tablename__ = "movies"

    name = Column(String, nullable=False)
    description = Column(String)
    posters = Column(ARRAY(String))
    genres = Column(ARRAY(String), nullable=False)
    release_date = Column(String, nullable=False)
    duration = Column(String, nullable=False)

    actors = relationship(
        "Actor", 
        secondary="movie_actors", 
        back_populates="movies", 
        cascade="all, delete", 
        passive_deletes=True
    )


class MovieActor(BaseModel):
    __tablename__ = "movie_actors"

    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    actor_id = Column(Integer, ForeignKey("actors.id", ondelete="CASCADE"), nullable=False, primary_key=True)