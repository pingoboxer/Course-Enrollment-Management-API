from fastapi import HTTPException
from app.core.storage import users


class UserService:

    @staticmethod
    def create_user(name: str, email: str, role: str):
        UserService._validate_name(name)
        UserService._validate_role(role)
        UserService._prevent_duplicate_email(email)

        user = {
            "id": len(users) + 1,
            "name": name.strip(),
            "email": email,
            "role": role
        }

        users.append(user)
        return user

    @staticmethod
    def get_all_users():
        return users

    @staticmethod
    def get_user_by_id(user_id: int):
        user = next((u for u in users if u["id"] == user_id), None)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    
    # Private Validation Methods

    @staticmethod
    def _validate_name(name: str):
        if not name or not name.strip():
            raise HTTPException(
                status_code=400,
                detail="Name must not be empty"
            )

    @staticmethod
    def _validate_role(role: str):
        if role not in ["student", "admin"]:
            raise HTTPException(
                status_code=400,
                detail="Role must be either 'student' or 'admin'"
            )

    @staticmethod
    def _prevent_duplicate_email(email: str):
        exists = any(u for u in users if u["email"] == email)
        if exists:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )
