from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.config.redis import redis_client
from app.schemas import auth as auth_schemas
from app.constants.envs import envs
from app.utils.auth.password import verify_password_hash
from .user import get_user_by_email_or_username

# Error Messages
INVALID_CREDENTIALS_MSG = "Invalid Email, Username, or Password."

def verify_user(db:Session, credentials:auth_schemas.Login):
    db_user = get_user_by_email_or_username(db, credentials.identifier)

    if not db_user or not verify_password_hash(credentials.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=INVALID_CREDENTIALS_MSG)

    return db_user

def login(db:Session, credentials:auth_schemas.Login):
    user = verify_user(db, credentials)

     # Check if the token is already cached in Redis
    cached_token = redis_client.get(f"user_token:{user.id}")

    if cached_token:
        return {
            "access_token": cached_token,
            "token_type": "bearer",
            "user": user
        }
    
    # Generate a new token
    from app.utils.auth.token import create_jwt

    jwt_token = create_jwt({"sub": str(user.id)})

     # Cache the new token in Redis with an expiration time
    token_expiration_seconds = envs.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    redis_client.setex(f"user_token:{user.id}", token_expiration_seconds, jwt_token)

    return {
        "access_token": jwt_token,
        "token_type": "bearer",
        "user": user
    }