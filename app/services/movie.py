from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError

from app.models import movie as models
from app.models import actor as actor_models
from app.schemas import movie as schemas


def get_movie(db:Session, movie_id:int):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()

def get_movies(db:Session, skip:int=0, limit:int=10):
    return db.query(models.Movie).offset(skip).limit(limit).all()

def create_movie(db:Session, movie:schemas.MovieCreate):
    db_movie = db.query(models.Movie).filter(models.Movie.name.ilike(movie.name)).first()
    if db_movie:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Movie already registered.")
    
    try:
        new_movie = models.Movie(
            name=movie.name,
            description=movie.description,
            posters=movie.posters,
            genres=movie.genres,
            release_date=movie.release_date,
            duration=movie.duration
        )
        db.add(new_movie)
        # just get the id of the new movie
        db.flush()

        for actor_id in movie.actors:
            db_actor = db.query(actor_models.Actor).filter(actor_models.Actor.id == actor_id).first()
            if not db_actor:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Actor not found.")
            new_movie.actors.append(db_actor)
        db.commit()
        db.refresh(new_movie)
        db_movie = db.query(models.Movie).options(joinedload(models.Movie.actors)).filter(models.Movie.id == new_movie.id).first()
        return db_movie
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating movie.")