from fastapi import APIRouter, Depends

from app.api.dependencies import (
    get_current_active_user,
    get_current_admin_user,
    get_user_service,
)
from app.models.user import User
from app.schemas.user import UserResponse
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get(
    "/me",
    response_model=UserResponse,
)
def read_current_user(
    current_user: User = Depends(get_current_active_user),
):
    return current_user

@router.get(
    "/",
    response_model=list[UserResponse],
)
def list_users(
    skip: int = 0,
    limit: int = 100,
    _: User = Depends(get_current_admin_user),
    service: UserService = Depends(get_user_service),
):
    return service.list_users(skip, limit)