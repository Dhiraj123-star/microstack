from pydantic import BaseModel, EmailStr
from typing import Optional


# Request body for creating/updating user
class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


# Response model
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True
