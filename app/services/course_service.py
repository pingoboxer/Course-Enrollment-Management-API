from fastapi import HTTPException
from app.core.storage import courses, enrollments


class CourseService:


    # Create Course

    @staticmethod
    def create_course(title: str, code: str, role: str):
        CourseService._ensure_admin(role)
        CourseService._validate_title(title)
        CourseService._validate_code(code)
        CourseService._prevent_duplicate_code(code)

        course = {
            "id": len(courses) + 1,
            "title": title.strip(),
            "code": code.strip().upper()
        }

        courses.append(course)
        return course


    # Get All Courses

    @staticmethod
    def get_all_courses():
        return courses

    
    # Get Course by ID

    @staticmethod
    def get_course_by_id(course_id: int):
        course = CourseService._find_course(course_id)
        return course
    
    @staticmethod
    def get_course_enrollments(course_id: int, role: str):
        CourseService._ensure_admin(role)
        CourseService._find_course(course_id)

        return [
            e for e in enrollments
            if e["course_id"] == course_id
        ]

    
    # Update Course

    @staticmethod
    def update_course(course_id: int, title: str, code: str, role: str):
        CourseService._ensure_admin(role)

        course = CourseService._find_course(course_id)

        if title:
            CourseService._validate_title(title)
            course["title"] = title.strip()

        if code:
            CourseService._validate_code(code)
            CourseService._prevent_duplicate_code(code, exclude_id=course_id)
            course["code"] = code.strip().upper()

        return course


    # Delete Course

    @staticmethod
    def delete_course(course_id: int, role: str):
        CourseService._ensure_admin(role)

        course = CourseService._find_course(course_id)
        global enrollments
        # Remove related enrollments
        enrollments[:] = [
            e for e in enrollments
            if e["course_id"] != course_id
        ]

        courses.remove(course)

        return {"message": "Course deleted successfully"}


    # Private Methods

    @staticmethod
    def _ensure_admin(role: str):
        if role != "admin":
            raise HTTPException(
                status_code=403,
                detail="Only admins allowed"
            )

    @staticmethod
    def _validate_title(title: str):
        if not title or not title.strip():
            raise HTTPException(
                status_code=400,
                detail="Course title must not be empty"
            )

    @staticmethod
    def _validate_code(code: str):
        if not code or not code.strip():
            raise HTTPException(
                status_code=400,
                detail="Course code must not be empty"
            )

    @staticmethod
    def _prevent_duplicate_code(code: str, exclude_id: int = None):
        code = code.strip().upper()

        for course in courses:
            if course["code"] == code:
                if exclude_id and course["id"] == exclude_id:
                    continue
                raise HTTPException(
                    status_code=400,
                    detail="Course code must be unique"
                )

    @staticmethod
    def _find_course(course_id: int):
        course = next((c for c in courses if c["id"] == course_id), None)
        if not course:
            raise HTTPException(
                status_code=404,
                detail="Course not found"
            )
        return course
