from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from app.schemas import seat as schemas
from app.services import seat as services

from app.dependencies import get_db, Auth


router = APIRouter(prefix="/seats", tags=["Seat"], dependencies=[Depends(Auth())])

@router.get('/', response_model=list[schemas.Seat])
def get_seats(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    seats = services.get_seats(db, skip, limit)
    return seats

@router.get('/{seat_id}', response_model=schemas.Seat)
def get_seat(seat_id: int, db: Session = Depends(get_db)):
    seat = services.get_seat(db, seat_id)
    return seat

@router.post('/', response_model=schemas.Seat)
def create_seat(payload: schemas.SeatCreate, db: Session = Depends(get_db)):
    seat = services.create_seat(db, payload)
    return seat

@router.put('/{seat_id}', response_model=schemas.Seat)
def update_seat(seat_id: int, payload: schemas.SeatUpdate, db: Session = Depends(get_db)):
    seat = services.update_seat(db, seat_id, payload)
    return seat

@router.delete('/{seat_id}')
def delete_seat(seat_id: int, db: Session = Depends(get_db)):
    services.delete_seat(db, seat_id)
    return JSONResponse({
        "detail": "Seat deleted successfully."
    })

@router.get('/theater/{theater_id}', response_model=list[schemas.Seat])
def get_seats_by_theater(theater_id: int, db: Session = Depends(get_db)):
    seats = services.get_seats_by_theater(db, theater_id)
    return seats