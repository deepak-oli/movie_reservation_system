from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas import user as schemas
from app.models import user as models
from app.utils.auth.password import get_password_hash

# Error Messages
EMAIL_ALREADY_REGISTERED = "Email already registered."
USERNAME_ALREADY_REGISTERED = "Username already registered."


def get_user(db:Session, user_id:int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db:Session, email:str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db:Session, username:str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email_or_username(db:Session, value:str):
    return db.query(models.User).filter((models.User.email == value) | (models.User.username == value)).first()

def create_user(db:Session, user:schemas.UserCreate):
    db_user = db.query(models.User).filter(
        (models.User.email == user.email) | (models.User.username == user.username)
    ).first()

    if db_user:
        if db_user.email == user.email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=EMAIL_ALREADY_REGISTERED)
        if db_user.username == user.username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=USERNAME_ALREADY_REGISTERED)
    
    hashed_password = get_password_hash(user.password)

    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    