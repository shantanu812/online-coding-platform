from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.submission import Submission


class SubmissionRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_submission(
        self,
        submission: Submission,
    ) -> Submission:
        
        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)

        return submission

    def get_submission_by_id(
        self,
        submission_id: int,
    ) -> Submission | None:
        
        statement = select(Submission).where(
            Submission.id == submission_id
        )

        return self.db.scalar(statement)

    def get_submissions_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Submission]:
        
        statement = (
            select(Submission)
            .where(Submission.user_id == user_id)
            .order_by(Submission.submitted_at.desc())
            .offset(skip)
            .limit(limit)
        )

        return list(self.db.scalars(statement).all())

    def get_submissions_by_problem(
        self,
        problem_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Submission]:
        
        statement = (
            select(Submission)
            .where(Submission.problem_id == problem_id)
            .order_by(Submission.submitted_at.desc())
            .offset(skip)
            .limit(limit)
        )

        return list(self.db.scalars(statement).all())

    def list_submissions(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Submission]:
        
        statement = (
            select(Submission)
            .order_by(Submission.submitted_at.desc())
            .offset(skip)
            .limit(limit)
        )

        return list(self.db.scalars(statement).all())

    def update_submission(
        self,
        submission: Submission,
    ) -> Submission:
      
        self.db.commit()
        self.db.refresh(submission)

        return submission