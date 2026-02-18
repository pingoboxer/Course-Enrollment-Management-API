
from pydantic import BaseModel


class CourseCreate(BaseModel):
    title: str
    code: str
    role: str

class CourseUpdate(BaseModel):
    title: str | None = None
    code: str | None = None
    role: str

class CourseResponse(BaseModel):
    id: int
    title: str
    code: str