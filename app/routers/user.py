from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.utils.misc.rate_limit import rate_limiter

from app.services import user as services
from app.schemas.user import ResetPassword, PasswordChange, AuthUser

from app.dependencies import get_db, Auth

router = APIRouter(prefix="/user", tags=["User"])

@router.post('/forgot-password')
@rate_limiter(rate_limit_count=2, rate_limit_window=60)
def forgot_password(email: str, request:Request, background_tasks: BackgroundTasks, db:Session = Depends(get_db)):
    user = services.forgot_password(db, email, background_tasks)
    return {
        "message": f"Password reset link sent to your emil {user.email}."
    }

@router.post('/reset-password')
def reset_password(payload:ResetPassword, db:Session = Depends(get_db)):

    if payload.password != payload.confirm_password:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match.") 

    user =  services.reset_password(db, payload.token, payload.password)
    return {
        "message": "Password reset successfully."
    }

@router.post('/change-password')
def change_password(payload:PasswordChange, user: AuthUser = Depends(Auth()),  db:Session = Depends(get_db)):
    # TODO: take old password as well and verify it
    if payload.password != payload.confirm_password:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match.") 

    user =  services.change_password(db, user.id, payload.password)
    return {
        "message": "Password changed successfully."
    }


    
