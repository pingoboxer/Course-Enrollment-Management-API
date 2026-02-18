from fastapi import APIRouter, status
from pydantic import BaseModel
from app.services.enrollment_service import EnrollmentService

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])


# Request Schemas

class EnrollmentRequest(BaseModel):
    user_id: int
    course_id: int
    role: str


class AdminForceDeregisterRequest(BaseModel):
    user_id: int
    course_id: int
    role: str


# Student Enrollment Endpoints

@router.post("", status_code=status.HTTP_201_CREATED)
def enroll(request: EnrollmentRequest):
    return EnrollmentService.enroll(
        user_id=request.user_id,
        course_id=request.course_id,
        role=request.role
    )


@router.delete("", status_code=status.HTTP_200_OK)
def deregister(request: EnrollmentRequest):
    return EnrollmentService.deregister(
        user_id=request.user_id,
        course_id=request.course_id,
        role=request.role
    )






# Admin Endpoints

@router.get("", status_code=status.HTTP_200_OK)
def get_all_enrollments(role: str):
    return EnrollmentService.get_all_enrollments(role)


@router.get("/courses/{course_id}", status_code=status.HTTP_200_OK)
def get_course_enrollments(course_id: int, role: str):
    return EnrollmentService.get_course_enrollments(course_id, role)


@router.delete("/admin/enrollments", status_code=status.HTTP_200_OK)
def force_deregister(request: AdminForceDeregisterRequest):
    return EnrollmentService.force_deregister(
        user_id=request.user_id,
        course_id=request.course_id,
        role=request.role
    )
