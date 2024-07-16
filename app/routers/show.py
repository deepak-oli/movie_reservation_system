from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from app.schemas import show as schemas
from app.services import show as services

from app.dependencies import get_db, Auth

router = APIRouter(prefix="/shows", tags=["Show"], dependencies=[Depends(Auth())])

@router.get('/', response_model=list[schemas.Show])
def get_shows(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    shows = services.get_shows(db, skip, limit)
    return shows

@router.get('/{show_id}', response_model=schemas.Show)
def get_show(show_id: int, db: Session = Depends(get_db)):
    show = services.get_show(db, show_id)
    return show

@router.post('/', response_model=schemas.Show)
def create_show(payload: schemas.ShowCreate, db: Session = Depends(get_db)):
    show = services.create_show(db, payload)
    return show

@router.put('/{show_id}', response_model=schemas.Show)
def update_show(show_id: int, payload: schemas.ShowUpdate, db: Session = Depends(get_db)):
    show = services.update_show(db, show_id, payload)
    return show

@router.delete('/{show_id}')
def delete_show(show_id: int, db: Session = Depends(get_db)):
    services.delete_show(db, show_id)
    return JSONResponse({
        "detail": "Show deleted successfully."
    })

@router.get('/theater/{theater_id}', response_model=list[schemas.Show])
def get_shows_by_theater(theater_id: int, db: Session = Depends(get_db)):
    shows = services.get_shows_by_theater(db, theater_id)
    return shows