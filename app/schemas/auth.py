from typing import Union
from pydantic import BaseModel, EmailStr, Field
from .user import UserResponse

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str = None

class Login(BaseModel):
    identifier: Union[str, EmailStr] = Field(..., description="A username or email address")
    password: str

class LoginResponse(Token):
    user: UserResponse



