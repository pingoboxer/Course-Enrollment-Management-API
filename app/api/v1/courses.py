from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.course_schema import (
    CourseCreate,
    CourseUpdate,
    CourseResponse,
    RoleRequest
)
from app.services.course_service import CourseService

router = APIRouter(prefix="/courses", tags=["Courses"])


# Public Access

@router.get("", response_model=List[CourseResponse], status_code=status.HTTP_200_OK)
def get_all_courses():
    return CourseService.get_all_courses()


@router.get("/{course_id}", response_model=CourseResponse, status_code=status.HTTP_200_OK)
def get_course(course_id: int):
    return CourseService.get_course_by_id(course_id)

@router.get("/{course_id}/enrollments")
def get_course_enrollments(course_id: int, role: str):
    return CourseService.get_course_enrollments(course_id, role)

# Admin Only

@router.post("", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(request: CourseCreate):
    return CourseService.create_course(
        title=request.title,
        code=request.code,
        role=request.role
    )


@router.put("/{course_id}", response_model=CourseResponse, status_code=status.HTTP_200_OK)
def update_course(course_id: int, request: CourseUpdate):
    return CourseService.update_course(
        course_id=course_id,
        title=request.title,
        code=request.code,
        role=request.role
    )


@router.delete("/{course_id}", status_code=status.HTTP_200_OK)
def delete_course(course_id: int, data: RoleRequest):
    if data.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete courses")
    return CourseService.delete_course(course_id, role=data.role)
