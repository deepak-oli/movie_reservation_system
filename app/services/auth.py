from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas import auth as auth_schemas
from .user import get_user_by_email_or_username


def verify_user(db:Session, credentials:auth_schemas.Login):
    db_user = get_user_by_email_or_username(db, credentials.identifier)

    error_msg = "Invalid Email, Username, or Password."

    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)

    from app.utils.auth.password import verify_password_hash
    if not verify_password_hash(credentials.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)

    return db_user

def login(db:Session, credentials:auth_schemas.Login):
    user = verify_user(db, credentials)
    
    from app.utils.auth.token import create_jwt

    jwt_token = create_jwt({"sub": str(user.id)})

    return {
        "access_token": jwt_token,
        "token_type": "bearer",
        "user": user
    }