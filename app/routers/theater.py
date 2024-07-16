from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from app.schemas import theater as schemas
from app.services import theater as services

from app.dependencies import get_db, Auth


router = APIRouter(prefix="/theaters", tags=["Theater"], dependencies=[Depends(Auth())])

@router.get('/', response_model=list[schemas.Theater])
def get_theaters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    theaters = services.get_theaters(db, skip, limit)
    return theaters

@router.get('/{theater_id}', response_model=schemas.Theater)
def get_theater(theater_id: int, db: Session = Depends(get_db)):
    theater = services.get_theater(db, theater_id)
    return theater

@router.post('/', response_model=schemas.Theater)
def create_theater(payload: schemas.TheaterCreate, db: Session = Depends(get_db)):
    theater = services.create_theater(db, payload)
    return theater

@router.put('/{theater_id}', response_model=schemas.Theater)
def update_theater(theater_id: int, payload: schemas.TheaterUpdate, db: Session = Depends(get_db)):
    theater = services.update_theater(db, theater_id, payload)
    return theater

@router.delete('/{theater_id}')
def delete_theater(theater_id: int, db: Session = Depends(get_db)):
    services.delete_theater(db, theater_id)
    return JSONResponse({
        "detail": "Theater deleted successfully."
    })

