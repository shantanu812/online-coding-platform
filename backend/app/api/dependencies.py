from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.auth.jwt import decode_access_token
from app.database.session import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.repositories.problem_repository import ProblemRepository
from app.services.problem_service import ProblemService
from app.repositories.test_case_repository import TestCaseRepository
from app.services.test_case_service import TestCaseService
from app.repositories.submission_repository import SubmissionRepository
from app.services.submission_service import SubmissionService
from app.services.judge_service import JudgeService
from app.repositories.contest_repository import ContestRepository
from app.services.contest_service import ContestService
from app.repositories.leaderboard_repository import LeaderboardRepository
from app.services.leaderboard_service import LeaderboardService

security = HTTPBearer()


def get_user_repository(
    db: Session = Depends(get_db),
) -> UserRepository:
    return UserRepository(db)


def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repository)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    service: UserService = Depends(get_user_service),
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
    )

    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(payload["sub"])

    except (JWTError, KeyError, ValueError):
        raise credentials_exception

    user = service.get_user_by_id(user_id)

    if user is None:
        raise credentials_exception

    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user.",
        )

    return current_user


def get_current_admin_user(
    current_user: User = Depends(get_current_active_user),
) -> User:

    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required.",
        )

    return current_user

def get_problem_repository(
    db: Session = Depends(get_db),
) -> ProblemRepository:
    return ProblemRepository(db)


def get_problem_service(
    repository: ProblemRepository = Depends(get_problem_repository),
) -> ProblemService:
    return ProblemService(repository)

def get_test_case_repository(
    db=Depends(get_db),
) -> TestCaseRepository:
    return TestCaseRepository(db)


def get_test_case_service(
    test_case_repository: TestCaseRepository = Depends(
        get_test_case_repository
    ),
    problem_repository: ProblemRepository = Depends(
        get_problem_repository
    ),
) -> TestCaseService:
    return TestCaseService(
        test_case_repository,
        problem_repository,
    )

def get_submission_repository(
    db=Depends(get_db),
) -> SubmissionRepository:
    return SubmissionRepository(db)


def get_submission_service(
    submission_repository: SubmissionRepository = Depends(
        get_submission_repository
    ),
    user_repository: UserRepository = Depends(
        get_user_repository
    ),
    problem_repository: ProblemRepository = Depends(
        get_problem_repository
    ),
) -> SubmissionService:
    return SubmissionService(
        submission_repository,
        user_repository,
        problem_repository,
    )

def get_judge_service(
    submission_repository: SubmissionRepository = Depends(
        get_submission_repository
    ),
    problem_repository: ProblemRepository = Depends(
        get_problem_repository
    ),
    test_case_repository: TestCaseRepository = Depends(
        get_test_case_repository
    ),
) -> JudgeService:
  
    return JudgeService(
        submission_repository=submission_repository,
        problem_repository=problem_repository,
        test_case_repository=test_case_repository,
    )

def get_contest_repository(
    db: Session = Depends(get_db),
) -> ContestRepository:
    return ContestRepository(db)


def get_contest_service(
    repository: ContestRepository = Depends(
        get_contest_repository,
    ),
) -> ContestService:
    return ContestService(repository)

def get_leaderboard_repository(
    db: Session = Depends(get_db),
) -> LeaderboardRepository:
    return LeaderboardRepository(db)


def get_leaderboard_service(
    repository: LeaderboardRepository = Depends(
        get_leaderboard_repository,
    ),
) -> LeaderboardService:
    return LeaderboardService(repository)