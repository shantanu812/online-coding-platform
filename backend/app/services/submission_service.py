from app.models.problem import Problem
from app.models.submission import (
    Submission,
    SubmissionStatus,
)
from app.models.user import User
from app.repositories.problem_repository import ProblemRepository
from app.repositories.submission_repository import SubmissionRepository
from app.repositories.user_repository import UserRepository
from app.schemas.submission import SubmissionCreate


class SubmissionService:
    
    SUPPORTED_LANGUAGES = {
        "python",
        "cpp",
        "java"
    }

    def __init__(
        self,
        submission_repository: SubmissionRepository,
        user_repository: UserRepository,
        problem_repository: ProblemRepository,
    ):
        self.submission_repository = submission_repository
        self.user_repository = user_repository
        self.problem_repository = problem_repository

    def create_submission(
        self,
        user_id: int,
        problem_id: int,
        submission_data: SubmissionCreate,
    ) -> Submission:
        

        user = self.user_repository.get_user_by_id(user_id)

        if user is None:
            raise ValueError("User not found.")

        problem = self.problem_repository.get_problem_by_id(
            problem_id
        )

        if problem is None:
            raise ValueError("Problem not found.")

        language = submission_data.language.strip().lower()

        if language not in self.SUPPORTED_LANGUAGES:
            raise ValueError(
                "Unsupported programming language."
            )

        if not submission_data.source_code.strip():
            raise ValueError(
                "Source code cannot be empty."
            )

        submission = Submission(
            user_id=user.id,
            problem_id=problem.id,
            language=language,
            source_code=submission_data.source_code,
            status=SubmissionStatus.PENDING,
        )

        return self.submission_repository.create_submission(
            submission
        )

    def get_submission(
        self,
        submission_id: int,
        current_user: User,
    ) -> Submission:
        

        submission = (
            self.submission_repository.get_submission_by_id(
                submission_id
            )
        )

        if submission is None:
            raise ValueError("Submission not found.")

        if (
            submission.user_id != current_user.id
            and not current_user.is_admin
        ):
            raise PermissionError(
                "You are not authorized to access this submission."
            )

        return submission

    def get_user_submissions(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Submission]:
        

        user = self.user_repository.get_user_by_id(user_id)

        if user is None:
            raise ValueError("User not found.")

        return self.submission_repository.get_submissions_by_user(
            user_id=user_id,
            skip=skip,
            limit=limit,
        )

    def get_problem_submissions(
        self,
        problem_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Submission]:
       

        problem = self.problem_repository.get_problem_by_id(
            problem_id
        )

        if problem is None:
            raise ValueError("Problem not found.")

        return (
            self.submission_repository.get_submissions_by_problem(
                problem_id=problem_id,
                skip=skip,
                limit=limit,
            )
        )

    def list_submissions(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Submission]:
       
        return self.submission_repository.list_submissions(
            skip=skip,
            limit=limit,
        )

    def update_submission(
        self,
        submission: Submission,
    ) -> Submission:
        

        return self.submission_repository.update_submission(
            submission
        )