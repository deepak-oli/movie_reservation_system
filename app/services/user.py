from sqlalchemy.orm import Session
from fastapi import HTTPException, status, BackgroundTasks

from app.schemas import user as schemas
from app.models import user as models
from app.utils.auth.password import get_password_hash
from app.utils.email.email_verification import confirm_verification_token, generate_verification_token, send_verification_email
from app.utils.email.forget_password import send_password_reset_email
from app.config.redis import redis_client
from app.utils.auth.token import decode_jwt, create_jwt
from app.utils.auth.password import verify_password_hash


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

def verify_email(db:Session, token:str):
    email = confirm_verification_token(token)
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token.")
    
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    
    user.is_active = True
    user.is_verified = True
    db.commit()
    db.refresh(user)
    return user

def forgot_password(db:Session, email:str, background_tasks:BackgroundTasks):
    user = get_user_by_email(db, email)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    # Generate a new token
    jwt_token = create_jwt({"sub": str(user.id)})

     # Cache the new token in Redis with an expiration time
    token_expiration_seconds = 24 * 60 * 60 # 24 hours
    redis_client.setex(f"user_token:{user.id}", token_expiration_seconds, jwt_token)

    background_tasks.add_task(send_password_reset_email, email, jwt_token, user.username)
    
    return user

def reset_password(db:Session, token:str, new_password:str):
    payload = decode_jwt(token)

    if not payload:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token.")
    
    user_id = payload.get("sub")

    cached_token = redis_client.get(f"user_token:{user_id}")

    if not cached_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token.")

    if not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token.")

    user = get_user(db, user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    
    
    is_same_as_previous = verify_password_hash(new_password, user.hashed_password)
    if is_same_as_previous:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="New password cannot be the same as the previous password."
        )

    new_hashed_password = get_password_hash(new_password)
    user.hashed_password = new_hashed_password
    db.commit()
    db.refresh(user)

    redis_client.delete(f"user_token:{user_id}")

    return user

def change_password(db:Session, user_id:int, new_password:str, old_password:str):
    user = get_user(db, user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    
    if not verify_password_hash(old_password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password.")
    
    is_same_as_previous = verify_password_hash(new_password, user.hashed_password)
    if is_same_as_previous:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="New password cannot be the same as the previous password."
        )

    new_hashed_password = get_password_hash(new_password)
    user.hashed_password = new_hashed_password
    db.commit()
    db.refresh(user)
    return user

def update_profile(db:Session, user_id:int, payload:schemas.UserUpdate, background_tasks:BackgroundTasks):
    user = get_user(db, user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        
    for key, value in vars(payload).items():
        if value is None:
            continue
        if key == "email":
            if value and user.email != value:
                setattr(user, 'is_verified', False)
                token = generate_verification_token(user.email)
                redis_client.setex(f"email_verification:{token}", 3600, user.email)
                background_tasks.add_task(send_verification_email, user.email, token, user.username)
        else:   
            setattr(user, key, value)
    
    db.commit()
    db.refresh(user)

    payload_email = payload.email
    if payload_email and user.email != payload_email:
        token = generate_verification_token(user.email)
        redis_client.setex(f"email_verification:{token}", 3600, user.email)
        background_tasks.add_task(send_verification_email, user.email, token, user.username)

    return user

def delete_user(db:Session, user_id:int):
    user = get_user(db, user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    
    db.delete(user)
    db.commit()
    return user