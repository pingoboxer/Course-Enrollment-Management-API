
from pydantic import BaseModel, Field
from app.schemas.common import UserRole


class CourseCreate(BaseModel):
    title: str = Field(..., min_length=1)
    code: str = Field(..., min_length=1)
    role: UserRole
    

class CourseUpdate(BaseModel):
    title: str | None = None
    code: str | None = None
    role: UserRole

class CourseResponse(BaseModel):
    id: int
    title: str
    code: str

class RoleRequest(BaseModel):
    role: UserRole
