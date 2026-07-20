from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.api.dependencies import (
    get_current_active_user,
    get_leaderboard_service,
)
from app.models.user import User
from app.schemas.leaderboard import (
    LeaderboardEntry,
    LeaderboardResponse,
    SubmissionStatistic,
)
from app.services.leaderboard_service import LeaderboardService

router = APIRouter(
    prefix="/contests",
    tags=["Leaderboard"],
)


@router.get(
    "/{contest_id}/leaderboard",
    response_model=LeaderboardResponse,
)
def get_leaderboard(
    contest_id: int,
    _: User = Depends(get_current_active_user),
    service: LeaderboardService = Depends(
        get_leaderboard_service,
    ),
):
    try:
        return service.generate_leaderboard(
            contest_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/{contest_id}/leaderboard/top/{limit}",
    response_model=LeaderboardResponse,
)
def get_top_leaderboard(
    contest_id: int,
    limit: int,
    _: User = Depends(get_current_active_user),
    service: LeaderboardService = Depends(
        get_leaderboard_service,
    ),
):
    try:
        leaderboard_data = service.generate_leaderboard(
            contest_id,
        )
        leaderboard_data.leaderboard = leaderboard_data.leaderboard[:limit]
        return leaderboard_data
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/{contest_id}/leaderboard/me",
    response_model=LeaderboardEntry,
)
def get_my_leaderboard_entry(
    contest_id: int,
    current_user: User = Depends(get_current_active_user),
    service: LeaderboardService = Depends(
        get_leaderboard_service,
    ),
):
    try:
        leaderboard_data = service.generate_leaderboard(
            contest_id,
        )
        for entry in leaderboard_data.leaderboard:
            if entry.user_id == current_user.id:
                return entry
                
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in leaderboard.",
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/{contest_id}/leaderboard/{user_id}/statistics",
    response_model=SubmissionStatistic,
)
def get_user_statistics(
    contest_id: int,
    user_id: int,
    _: User = Depends(get_current_active_user),
    service: LeaderboardService = Depends(
        get_leaderboard_service,
    ),
):
    try:
        leaderboard_data = service.generate_leaderboard(
            contest_id,
        )
        for entry in leaderboard_data.leaderboard:
            if entry.user_id == user_id:
                return entry.statistics
                
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in leaderboard.",
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )