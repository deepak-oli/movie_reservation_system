from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.utils.misc.rate_limit import rate_limiter

from app.services import user as services
from app.schemas.user import ResetPassword, ChangePasswordRequest, AuthUser,UserUpdate

from app.dependencies import get_db, Auth

router = APIRouter(prefix="/user", tags=["User"])

@router.patch('/update-profile', response_model=AuthUser)
def update_profile(payload:UserUpdate, background_tasks: BackgroundTasks, user: AuthUser = Depends(Auth()), db:Session = Depends(get_db)):
    user = services.update_profile(db, user.id, payload, background_tasks)
    return user


@router.post('/forgot-password')
@rate_limiter(rate_limit_count=2, rate_limit_window=60)
def forgot_password(email: str, request:Request, background_tasks: BackgroundTasks, db:Session = Depends(get_db)):
    user = services.forgot_password(db, email, background_tasks)
    return JSONResponse({
        "detail": f"Password reset link sent to your emil {user.email}."
    })

@router.post('/reset-password')
def reset_password(payload:ResetPassword, db:Session = Depends(get_db)):

    if payload.new_password != payload.confirm_new_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match.") 

    user =  services.reset_password(db, payload.token, payload.new_password)
    return JSONResponse({"detail": "Password reset successfully."})

@router.post('/change-password')
def change_password(payload:ChangePasswordRequest, user: AuthUser = Depends(Auth()),  db:Session = Depends(get_db)):
    if payload.new_password != payload.confirm_new_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match.") 

    user =  services.change_password(db, user.id, payload.new_password, payload.old_password)
    return JSONResponse({"detail": "Password changed successfully."})


    
