from pydantic import BaseModel, EmailStr
from typing import Optional, List
from uuid import UUID


class RegisterRequest(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str
    name: Optional[str] = None
    referrer: Optional[str] = None


class RegisterResponse(BaseModel):
    data: dict


class LoginRequest(BaseModel):
    identifier: str # email or phone
    password: str


class LoginResponse(BaseModel):
    data: dict