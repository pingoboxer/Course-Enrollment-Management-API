from fastapi import APIRouter, status
from typing import List
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])



# Create User

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(request: UserCreate):
    return UserService.create_user(
        name=request.name,
        email=request.email,
        role=request.role
    )


# Get All Users

@router.get("", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def get_all_users():
    return UserService.get_all_users()



# Get User by ID

@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(user_id: int):
    return UserService.get_user_by_id(user_id)
