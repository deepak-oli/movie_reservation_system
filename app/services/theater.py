from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


from app.schemas import theater as schemas
from app.models import theater as models

def get_theater(db: Session, theater_id: int):
    theater = db.query(models.Theater).filter(models.Theater.id == theater_id).first()
    if theater is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Theater not found.")
    return theater

def get_theaters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Theater).offset(skip).limit(limit).all()

def create_theater(db: Session, theater: schemas.TheaterCreate):
    db_theater = models.Theater(**theater.model_dump())
    db.add(db_theater)
    db.commit()
    db.refresh(db_theater)
    return db_theater

def update_theater(db: Session, theater_id: int, theater: schemas.TheaterUpdate):
    db_theater = get_theater(db, theater_id)
    for key, value in vars(theater).items():
        setattr(db_theater, key, value)
    db.commit()
    db.refresh(db_theater)
    return db_theater

def delete_theater(db: Session, theater_id: int):
    db_theater = get_theater(db, theater_id)
    db.delete(db_theater)
    db.commit()
    return db_theater

