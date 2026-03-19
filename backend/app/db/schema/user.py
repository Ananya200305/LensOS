from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Union
import re

PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$"

class UserInCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        if not re.match(PASSWORD_REGEX, value):
            raise ValueError("Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, one number, and one special character.")
        return value
    
    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_name(cls, value):
        value = value.strip()
        if not value.isalpha():
            raise ValueError("Name must contain only alphabetic characters.")
        return value

class UserOutput(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr

class UserInUpdate(BaseModel):
    id: int
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    email: Union[EmailStr, None] = None
    password: Union[str, None] = None

    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        if value is not None and not re.match(PASSWORD_REGEX, value):
            raise ValueError("Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, one number, and one special character.")
        return value

class UserInLogin(BaseModel):
    email: EmailStr
    password: str

class UserWithToken(BaseModel):
    token: str