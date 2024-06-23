from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

from app.constants.envs import envs

SECRET_KEY = envs.SECRET_KEY

if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for JWT token generation")

ALGORITHM = "HS256"

def create_jwt(data: dict, expires_delta: timedelta = envs.ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    else:
        expire = datetime.now() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_jwt(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = datetime.fromtimestamp(decoded_token["exp"], tz=timezone.utc)
        return decoded_token if exp >= datetime.now(timezone.utc) else None
    except JWTError as e:
        return None
    
