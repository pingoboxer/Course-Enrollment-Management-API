
from pydantic import BaseModel


class CourseCreate(BaseModel):
    title: str
    code: str
