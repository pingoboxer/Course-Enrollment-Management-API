
from pydantic import BaseModel


class EnrollmentCreate(BaseModel):
    user_id: int
    course_id: int

class RoleRequest(BaseModel):
    role: str
