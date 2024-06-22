from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer

from typing import Optional

from app.utils.auth.token import decode_jwt

from app.services.user import get_user

from app.config.redis import get_redis_client
from app.config.db import get_db

ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def is_token_blacklisted(token: str, redis_client = Depends(get_redis_client)):
    return redis_client.get(token) == 'blacklisted'

class Auth(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(Auth, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(Auth, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication scheme.")
            payload = self.verify_token(credentials.credentials)
            if not payload:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token or expired token.")
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token or expired token.")
            db = next(get_db())
            db_user = get_user(db, user_id)
            if not db_user:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="User not found.")
            if db_user.is_active == False:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="User is not active.")
            if db_user.is_verified == False:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="User is not verified.")
            request.state.user = db_user
            return db_user
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization code.")
        
    def verify_token(self, token: str) -> Optional[dict]:
        try:
            payload = decode_jwt(token)
        except:
            payload = None
        return payload
