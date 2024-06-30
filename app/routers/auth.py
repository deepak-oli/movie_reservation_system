from fastapi import APIRouter, Depends, BackgroundTasks,HTTPException, status, Request
from sqlalchemy.orm import Session

from app.dependencies import get_db, Auth
from app.config.redis import redis_client

from app.schemas import user as schemas
from app.schemas import auth as auth_schemas

from app.services import user as services
from app.services import auth as auth_services
from app.utils.email.email_verification import generate_verification_token, send_verification_email
from app.utils.misc.rate_limit import rate_limiter

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post('/register/', response_model=schemas.UserResponse)
async def register_user(user: schemas.UserCreate, background_tasks:BackgroundTasks, db:Session = Depends(get_db)):
    new_user =  services.create_user(db, user)

    token = generate_verification_token(new_user.email)
    redis_client.setex(f"email_verification:{token}", 3600, new_user.email)

    background_tasks.add_task(send_verification_email, new_user.email, token, new_user.username)
    return new_user

@router.post('/login/', response_model=auth_schemas.LoginResponse)
def login_user(
    credentials: auth_schemas.Login, 
    db:Session = Depends(get_db)
):
    return auth_services.login(db, credentials)

@router.post('/verify-email/', response_model=schemas.UserResponse)
async def verify_email(
    token: str,
    db: Session = Depends(get_db)
):
    cached_email = redis_client.get(f"email_verification:{token}")
    if not cached_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or already used token.")
    
    email = services.verify_email(db, token)
    # Invalidate the token by deleting it
    redis_client.delete(f"email_verification:{token}")
    return email

@router.post('/resent-verification-email/', response_model=schemas.UserResponse)
@rate_limiter(rate_limit_count=2, rate_limit_window=60)
def resent_verification_email(
    email: str,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    user = services.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    
    if user.is_verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already verified.")
    
    token = generate_verification_token(user.email)
    redis_client.setex(f"email_verification:{token}", 3600, email)

    background_tasks.add_task(send_verification_email, user.email, token, user.username)
    return user

@router.get('/me/', response_model=schemas.UserResponse)
def get_me(
    user: schemas.AuthUser = Depends(Auth())
):
    return user

# TOOD
# social login
# 2FA
# refresh token