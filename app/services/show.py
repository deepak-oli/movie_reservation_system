from sqlalchemy.orm import Session
from fastapi import HTTPException, status


from app.schemas import show as schemas
from app.models import show as models

from app.models.theater import Theater
from app.services.movies import get_movie_details

def get_show(db: Session, show_id: int):
    show = db.query(models.Show).filter(models.Show.id == show_id).first()
    if show is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Show not found.")
    return show

def get_shows(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Show).offset(skip).limit(limit).all()

def create_show(db: Session, show: schemas.ShowCreate):
    # verify movie_id
    try:
        movie = get_movie_details(show.movie_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found.")
    
    # verify theater_id
    theater = db.query(Theater).filter(Theater.id == show.theater_id).first()
    if theater is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Theater not found.")

    db_show = models.Show(**show.model_dump())
    db.add(db_show)
    db.commit()
    db.refresh(db_show)
    return db_show

def update_show(db: Session, show_id: int, show: schemas.ShowUpdate):
    # verify movie_id
    movie = get_movie_details(show.movie_id)
    if isinstance(movie, HTTPException):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found.")
    
    db_show = get_show(db, show_id)
    for key, value in vars(show).items():
        setattr(db_show, key, value)
    db.commit()
    db.refresh(db_show)
    return db_show

def delete_show(db: Session, show_id: int):
    db_show = get_show(db, show_id)
    db.delete(db_show)
    db.commit()
    return db_show

def get_shows_by_theater(db: Session, theater_id: int):
    return db.query(models.Show).filter(models.Show.theater_id == theater_id).all()