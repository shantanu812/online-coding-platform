from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.api.dependencies import (
    get_current_active_user,
    get_current_admin_user,
    get_submission_service,
)
from app.models.user import User
from app.schemas.submission import (
    SubmissionCreate,
    SubmissionListResponse,
    SubmissionResponse,
)
from app.services.submission_service import SubmissionService

router = APIRouter(
    tags=["Submissions"],
)

@router.post(
    "/problems/{problem_id}/submit",
    response_model=SubmissionResponse,
    status_code=status.HTTP_201_CREATED,
)
def submit_solution(
    problem_id: int,
    submission_data: SubmissionCreate,
    current_user: User = Depends(get_current_active_user),
    service: SubmissionService = Depends(get_submission_service),
):
    try:
        return service.create_submission(
            user_id=current_user.id,
            problem_id=problem_id,
            submission_data=submission_data,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
@router.get(
    "/submissions/{submission_id}",
    response_model=SubmissionResponse,
)
def get_submission(
    submission_id: int,
    current_user: User = Depends(get_current_active_user),
    service: SubmissionService = Depends(get_submission_service),
):
    try:
        return service.get_submission(
            submission_id,
            current_user,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )

@router.get(
    "/users/me/submissions",
    response_model=list[SubmissionListResponse],
)
def get_my_submissions(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    service: SubmissionService = Depends(get_submission_service),
):
    try:
        return service.get_user_submissions(
            user_id=current_user.id,
            skip=skip,
            limit=limit,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

@router.get(
    "/submissions",
    response_model=list[SubmissionListResponse],
)
def list_submissions(
    skip: int = 0,
    limit: int = 100,
    _: User = Depends(get_current_admin_user),
    service: SubmissionService = Depends(get_submission_service),
):
    return service.list_submissions(
        skip=skip,
        limit=limit,
    )

@router.get(
    "/problems/{problem_id}/submissions",
    response_model=list[SubmissionListResponse],
)
def get_problem_submissions(
    problem_id: int,
    skip: int = 0,
    limit: int = 100,
    _: User = Depends(get_current_admin_user),
    service: SubmissionService = Depends(get_submission_service),
):
    try:
        return service.get_problem_submissions(
            problem_id=problem_id,
            skip=skip,
            limit=limit,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
