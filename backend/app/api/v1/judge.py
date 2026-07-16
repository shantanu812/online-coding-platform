from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
import traceback
from app.api.dependencies import get_judge_service
from app.api.dependencies import get_current_admin_user
from app.schemas.submission import SubmissionResponse
from app.services.judge_service import JudgeService

router = APIRouter(
    prefix="/submissions",
    tags=["Online Judge"],
)


@router.post(
    "/{submission_id}/judge",
    response_model=SubmissionResponse,
    status_code=status.HTTP_200_OK,
)
def judge_submission(
    submission_id: int,
    judge_service: JudgeService = Depends(
        get_judge_service
    ),
    _: dict = Depends(
        get_current_admin_user
    ),
):

    try:
        return judge_service.judge_submission(
            submission_id
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )

    except Exception as exc:
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )