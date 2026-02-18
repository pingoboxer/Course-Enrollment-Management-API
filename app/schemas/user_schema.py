from pydantic import BaseModel, EmailStr, Field
from app.schemas.common import UserRole

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    role: UserRole

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole