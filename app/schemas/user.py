import re
from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationError
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=25)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=25)

    @field_validator('username')
    def validate_username(cls, v):
        if not 3 <= len(v) <= 25:
            raise ValueError('Username must be 3-25 chars.')
        if not re.match(r'^[a-zA-Z_]', v):
            raise ValueError('Username must start with an alphabet or an underscore.')
        if not re.search(r'[a-zA-Z]', v):
            raise ValueError('Username must contain at least one letter')
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username must contain only letters, numbers, and underscores.')
        return v
    
    @field_validator('password')
    def validate_password(cls, v):
        if not re.match(r'^(?=.*[A-Z])(?=.*[!@#$%^&*(),.?":{}|<>])(?=.*[a-zA-Z])(?=.*\d)[A-Za-z\d!@#$%^&*(),.?":{}|<>]{6,25}$', v):
            raise ValueError('Password must be 6-25 chars, with uppercase, special char, letter, and number.')
        return v

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool
    is_verified: bool

class AuthUser(UserResponse):
    is_active: bool


class PasswordChange(BaseModel):
    password: str = Field(..., min_length=6, max_length=25)
    confirm_password: str = Field(..., min_length=6, max_length=25)

    @field_validator('password')
    def validate_password(cls, v):
        if not re.match(r'^(?=.*[A-Z])(?=.*[!@#$%^&*(),.?":{}|<>])(?=.*[a-zA-Z])(?=.*\d)[A-Za-z\d!@#$%^&*(),.?":{}|<>]{6,25}$', v):
            raise ValueError('Password must be 6-25 chars, with uppercase, special char, letter, and number.')
        return v
class ResetPassword(PasswordChange):
    token: str
    