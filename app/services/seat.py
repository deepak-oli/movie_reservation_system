from sqlalchemy.orm import Session
from fastapi import HTTPException, status


from app.schemas import seat as schemas
from app.models import seat as models

from app.models.theater import Theater

def get_seat(db: Session, seat_id: int):
    seat = db.query(models.Seat).filter(models.Seat.id == seat_id).first()
    if seat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seat not found.")
    return seat

def get_seats(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Seat).offset(skip).limit(limit).all()

def create_seat(db: Session, seat: schemas.SeatCreate):
    # verify theater_id
    theater = db.query(Theater).filter(Theater.id == seat.theater_id).first()
    if theater is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Theater not found.")

    db_seat = models.Seat(**seat.model_dump())
    db.add(db_seat)
    db.commit()
    db.refresh(db_seat)
    return db_seat

def update_seat(db: Session, seat_id: int, seat: schemas.SeatUpdate):
    # verify theater_id
    theater = db.query(Theater).filter(Theater.id == seat.theater_id).first()
    if theater is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Theater not found.")
    
    db_seat = get_seat(db, seat_id)
    for key, value in vars(seat).items():
        setattr(db_seat, key, value)
    db.commit()
    db.refresh(db_seat)
    return db_seat

def delete_seat(db: Session, seat_id: int):
    db_seat = get_seat(db, seat_id)
    db.delete(db_seat)
    db.commit()
    return db_seat

def get_seats_by_theater(db: Session, theater_id: int):
    return db.query(models.Seat).filter(models.Seat.theater_id == theater_id).all()