from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import Auth, get_db
from app.services import movie as services
from app.schemas import movie as schemas


router = APIRouter(prefix='/movies',tags=["Movies"], dependencies=[Depends(Auth())])

@router.get("/", response_model=list[schemas.Movie])
def get_movies(skip:int=0, limit:int=10, db: Session = Depends(get_db)):
    return services.get_movies(db, skip, limit)

@router.get("/{movie_id}", response_model=schemas.Movie)
def get_movie(movie_id:int, db: Session = Depends(get_db)):
    movie = services.get_movie(db, movie_id)
    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found.")
    return movie

@router.post("/", response_model=schemas.Movie)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    return services.create_movie(db, movie)

