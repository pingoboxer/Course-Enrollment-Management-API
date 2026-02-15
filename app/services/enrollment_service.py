from fastapi import HTTPException
from app.core.storage import users, courses, enrollments


class EnrollmentService:

    @staticmethod
    def enroll(user_id: int, course_id: int, role: str):
        EnrollmentService._ensure_student_role(role)
        user = EnrollmentService._get_user(user_id)
        course = EnrollmentService._get_course(course_id)
        EnrollmentService._prevent_duplicate(user_id, course_id)

        enrollment = {
            "id": len(enrollments) + 1,
            "user_id": user_id,
            "course_id": course_id
        }

        enrollments.append(enrollment)
        return enrollment

    @staticmethod
    def deregister(user_id: int, course_id: int, role: str):
        EnrollmentService._ensure_student_role(role)

        enrollment = EnrollmentService._find_enrollment(user_id, course_id)

        enrollments.remove(enrollment)
        return {"message": "Deregistered successfully"}

    @staticmethod
    def get_student_enrollments(user_id: int):
        EnrollmentService._get_user(user_id)

        return [
            e for e in enrollments
            if e["user_id"] == user_id
        ]

    @staticmethod
    def get_all_enrollments(role: str):
        EnrollmentService._ensure_admin_role(role)
        return enrollments

    @staticmethod
    def get_course_enrollments(course_id: int, role: str):
        EnrollmentService._ensure_admin_role(role)
        EnrollmentService._get_course(course_id)

        return [
            e for e in enrollments
            if e["course_id"] == course_id
        ]

    @staticmethod
    def force_deregister(user_id: int, course_id: int, role: str):
        EnrollmentService._ensure_admin_role(role)

        enrollment = EnrollmentService._find_enrollment(user_id, course_id)
        enrollments.remove(enrollment)

        return {"message": "Student forcefully deregistered"}

    
    # Private Validation Methods

    @staticmethod
    def _ensure_student_role(role: str):
        if role != "student":
            raise HTTPException(status_code=403, detail="Only students allowed")

    @staticmethod
    def _ensure_admin_role(role: str):
        if role != "admin":
            raise HTTPException(status_code=403, detail="Only admins allowed")

    @staticmethod
    def _get_user(user_id: int):
        user = next((u for u in users if u["id"] == user_id), None)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    def _get_course(course_id: int):
        course = next((c for c in courses if c["id"] == course_id), None)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        return course

    @staticmethod
    def _prevent_duplicate(user_id: int, course_id: int):
        exists = any(
            e for e in enrollments
            if e["user_id"] == user_id and e["course_id"] == course_id
        )
        if exists:
            raise HTTPException(
                status_code=400,
                detail="Student already enrolled in this course"
            )

    @staticmethod
    def _find_enrollment(user_id: int, course_id: int):
        enrollment = next(
            (e for e in enrollments
             if e["user_id"] == user_id and e["course_id"] == course_id),
            None
        )
        if not enrollment:
            raise HTTPException(
                status_code=404,
                detail="Enrollment not found"
            )
        return enrollment
