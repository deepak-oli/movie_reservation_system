import re
from pydantic import BaseModel, EmailStr, Field, field_validator

# Common password validation logic
def validate_password(value: str) -> str:
    pattern = r'^(?=.*[A-Z])(?=.*[!@#$%^&*(),.?":{}|<>])(?=.*[a-zA-Z])(?=.*\d)[A-Za-z\d!@#$%^&*(),.?":{}|<>]{6,25}$'
    if not re.match(pattern, value):
        raise ValueError('Password must be 6-25 characters long, include an uppercase letter, a special character, a letter, and a number.')
    return value

# Common username validation logic
def validate_username(value: str) -> str:
    if not 3 <= len(value) <= 25:
        raise ValueError('Username must be between 3 and 25 characters.')
    if not re.match(r'^[a-zA-Z_]', value):
        raise ValueError('Username must start with a letter or an underscore.')
    if not re.search(r'[a-zA-Z]', value):
        raise ValueError('Username must contain at least one letter.')
    if not re.match(r'^[a-zA-Z0-9_]+$', value):
        raise ValueError('Username can only contain letters, numbers, and underscores.')
    return value

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=25)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=25)

    @field_validator('username')
    def validate_username_field(cls, v):
        return validate_username(v)
    
    @field_validator('password')
    def validate_password_field(cls, v):
        return validate_password(v)

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
    new_password: str = Field(..., min_length=6, max_length=25)
    confirm_new_password: str = Field(..., min_length=6, max_length=25)

    @field_validator('new_password')
    def validate_password(cls, v):
        return validate_password(v)
    
class ChangePasswordRequest(PasswordChange):
    old_password: str = Field(..., min_length=6, max_length=25)

    @field_validator('old_password')
    def validate_old_password(cls, v):
        return validate_password(v)
    
class ResetPassword(PasswordChange):
    token: str

class UserUpdate(BaseModel):
    username: str = None
    email: EmailStr = None

    @field_validator('username', mode="before")
    def validate_username_field(cls, v):
        if v is None:
            return v
        return validate_username(v)
    
        