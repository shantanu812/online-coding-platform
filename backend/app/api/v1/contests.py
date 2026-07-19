from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.api.dependencies import get_contest_service
from app.api.dependencies import (
    get_current_active_user,
    get_current_admin_user,
)
from app.models.user import User
from app.schemas.contest import (
    ContestCreate,
    ContestProblemAdd,
    ContestRegistration,
    ContestResponse,
    ContestUpdate,
)
from app.services.contest_service import ContestService

router = APIRouter(
    prefix="/contests",
    tags=["Contests"],
)


@router.post(
    "",
    response_model=ContestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_contest(
    contest_data: ContestCreate,
    current_user: User = Depends(
        get_current_admin_user,
    ),
    service: ContestService = Depends(
        get_contest_service,
    ),
):
    try:
        return service.create_contest(
            contest_data,
            current_user.id,
        )
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.put(
    "/{contest_id}",
    response_model=ContestResponse,
)
def update_contest(
    contest_id: int,
    contest_data: ContestUpdate,
    _: User = Depends(get_current_admin_user),
    service: ContestService = Depends(
        get_contest_service,
    ),
):
    try:
        return service.update_contest(
            contest_id,
            contest_data,
        )
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.delete(
    "/{contest_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_contest(
    contest_id: int,
    _: User = Depends(get_current_admin_user),
    service: ContestService = Depends(
        get_contest_service,
    ),
):
    try:
        service.delete_contest(contest_id)
    except ValueError as e:
        raise HTTPException(404, str(e))


@router.get(
    "/{contest_id}",
    response_model=ContestResponse,
)
def get_contest(
    contest_id: int,
    _: User = Depends(get_current_active_user),
    service: ContestService = Depends(
        get_contest_service,
    ),
):
    try:
        return service.get_contest(contest_id)
    except ValueError as e:
        raise HTTPException(404, str(e))


@router.get(
    "",
    response_model=list[ContestResponse],
)
def list_contests(
    skip: int = 0,
    limit: int = 100,
    _: User = Depends(get_current_active_user),
    service: ContestService = Depends(
        get_contest_service,
    ),
):
    return service.list_contests(skip, limit)


@router.post(
    "/register",
    status_code=status.HTTP_200_OK,
)
def register_contest(
    registration: ContestRegistration,
    current_user: User = Depends(
        get_current_active_user,
    ),
    service: ContestService = Depends(
        get_contest_service,
    ),
):
    try:
        service.register_user(
            registration.contest_id,
            current_user.id,
        )
        return {
            "message": "Registered successfully."
        }
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.post(
    "/{contest_id}/problems",
)
def add_problem(
    contest_id: int,
    request: ContestProblemAdd,
    _: User = Depends(get_current_admin_user),
    service: ContestService = Depends(
        get_contest_service,
    ),
):
    try:
        service.add_problem(
            contest_id,
            request.problem_id,
        )
        return {
            "message": "Problem added successfully."
        }
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.delete(
    "/{contest_id}/problems/{problem_id}",
)
def remove_problem(
    contest_id: int,
    problem_id: int,
    _: User = Depends(get_current_admin_user),
    service: ContestService = Depends(
        get_contest_service,
    ),
):
    try:
        service.remove_problem(
            contest_id,
            problem_id,
        )
        return {
            "message": "Problem removed successfully."
        }
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get(
    "/{contest_id}/problems",
)
def list_problems(
    contest_id: int,
    _: User = Depends(get_current_active_user),
    service: ContestService = Depends(
        get_contest_service,
    ),
):
    try:
        return service.get_contest_problems(
            contest_id,
        )
    except ValueError as e:
        raise HTTPException(404, str(e))


@router.get(
    "/{contest_id}/participants",
)
def list_participants(
    contest_id: int,
    _: User = Depends(get_current_admin_user),
    service: ContestService = Depends(
        get_contest_service,
    ),
):
    try:
        return service.get_contest_participants(
            contest_id,
        )
    except ValueError as e:
        raise HTTPException(404, str(e))