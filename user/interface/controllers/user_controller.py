from dependency_injector.wiring import inject, Provide
from containers import Container
from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr, Field
from user.application.user_service import UserService
from datetime import datetime

router = APIRouter(prefix="/users")

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime
    updated_at: datetime

class CreateUserBody(BaseModel):
    name: str = Field(min_length=2, max_length=32)
    email:EmailStr = Field(max_length=64)
    password: str = Field(min_length=8, max_length=32)


@router.post("", status_code=201, response_model=UserResponse)
@inject
def create_user(
    user: CreateUserBody,
    user_service: UserService = Depends(Provide[Container.user_service]),
    # user_service: UserService = Depends(Provide["user_service"]),
):
    created_user = user_service.create_user(
        # background_tasks=background_tasks,
        name=user.name,
        email=user.email,
        password=user.password,
    )

    return created_user

class UpdateUser(BaseModel):
    name: str | None = Field(min_length=2, max_length=32, default=None)
    password: str | None = Field(min_length=8, max_length=32, default=None)

@router.put("/{user_id}")
@inject
def update_user(user_id: str, user: UpdateUser, user_service: UserService = Depends(Provide[Container.user_service])):
    user = user_service.update_user(
        user_id=user_id,
        name=user.name,
        password=user.password
    )

    return user

class GetUserResponse(BaseModel):
    total_count: int
    page: int
    users: list[UserResponse]

@router.get("", response_model=GetUserResponse)
@inject
def get_users(page: int = 1, items_per_page: int = 10, user_service: UserService = Depends(Provide[Container.user_service])):


    total_count, users = user_service.get_users(page, items_per_page)

    return {
        "total_count": total_count,
        "page": page,
        "users": users,
        }

@router.delete("", status_code=204)
@inject
def delete_user(user_id: str, user_service: UserService = Depends(Provide[Container.user_service])):
    user_service.delete_user(user_id)