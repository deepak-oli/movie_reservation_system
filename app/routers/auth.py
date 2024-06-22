from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db, Auth

from app.schemas import user as schemas
from app.schemas import auth as auth_schemas

from app.services import user as services
from app.services import auth as auth_services
from app.utils.email import generate_verification_token, send_verification_email

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post('/register/', response_model=schemas.UserResponse)
async def register_user(user: schemas.UserCreate, db:Session = Depends(get_db)):
    new_user =  services.create_user(db, user)

    token = generate_verification_token(new_user.email)
    await send_verification_email(new_user.email, token, new_user.username)

    return new_user

@router.post('/login/', response_model=auth_schemas.LoginResponse)
def login_user(
    credentials: auth_schemas.Login, 
    db:Session = Depends(get_db)
):
    return auth_services.login(db, credentials)

@router.get('/me/', response_model=schemas.UserResponse)
def get_me(
    user: schemas.AuthUser = Depends(Auth())
):
    return user


