from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import (
    get_current_active_user,
    get_current_admin_user,
    get_problem_service,
)
from app.models.user import User
from app.schemas.problem import (
    ProblemCreate,
    ProblemListResponse,
    ProblemResponse,
    ProblemUpdate,
)
from app.services.problem_service import ProblemService

router = APIRouter(
    prefix="/problems",
    tags=["Problems"],
)


@router.post(
    "",
    response_model=ProblemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_problem(
    problem_data: ProblemCreate,
    current_user: User = Depends(get_current_admin_user),
    service: ProblemService = Depends(get_problem_service),
):
    try:
        return service.create_problem(
            problem_data,
            current_user.id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "",
    response_model=list[ProblemListResponse],
)
def list_problems(
    skip: int = 0,
    limit: int = 100,
    _: User = Depends(get_current_active_user),
    service: ProblemService = Depends(get_problem_service),
):
    return service.list_problems(skip, limit)


@router.get(
    "/{problem_id}",
    response_model=ProblemResponse,
)
def get_problem(
    problem_id: int,
    _: User = Depends(get_current_active_user),
    service: ProblemService = Depends(get_problem_service),
):
    try:
        return service.get_problem(problem_id)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get(
    "/slug/{slug}",
    response_model=ProblemResponse,
)
def get_problem_by_slug(
    slug: str,
    _: User = Depends(get_current_active_user),
    service: ProblemService = Depends(get_problem_service),
):
    try:
        return service.get_problem_by_slug(slug)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.put(
    "/{problem_id}",
    response_model=ProblemResponse,
)
def update_problem(
    problem_id: int,
    problem_data: ProblemUpdate,
    _: User = Depends(get_current_admin_user),
    service: ProblemService = Depends(get_problem_service),
):
    try:
        return service.update_problem(
            problem_id,
            problem_data,
        )

    except ValueError as e:
        message = str(e)

        status_code = (
            status.HTTP_404_NOT_FOUND
            if message == "Problem not found."
            else status.HTTP_400_BAD_REQUEST
        )

        raise HTTPException(
            status_code=status_code,
            detail=message,
        )


@router.delete(
    "/{problem_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_problem(
    problem_id: int,
    _: User = Depends(get_current_admin_user),
    service: ProblemService = Depends(get_problem_service),
):
    try:
        service.delete_problem(problem_id)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )