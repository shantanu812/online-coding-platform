from sqlalchemy import select
from sqlalchemy.orm import (
    Session,
    joinedload,
    selectinload,
)
from collections import defaultdict
from app.models.contest import Contest
from app.models.user import User
from app.models.problem import Problem
from app.models.submission import (
    Submission,
    SubmissionVerdict,
)


class LeaderboardRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def get_contest_by_id(
        self,
        contest_id: int,
    ) -> Contest | None:

        statement = (
            select(Contest)
            .where(Contest.id == contest_id)
            .options(
                selectinload(Contest.participants),
                selectinload(Contest.problems),
            )
        )

        return self.db.scalar(statement)

    def get_contest_participants(
        self,
        contest_id: int,
    ) -> list[User]:

        statement = (
            select(User)
            .join(User.contests)
            .where(Contest.id == contest_id)
            .order_by(User.id)
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_contest_problems(
        self,
        contest_id: int,
    ) -> list[Problem]:
      

        statement = (
            select(Problem)
            .join(Problem.contests)
            .where(Contest.id == contest_id)
            .order_by(Problem.id)
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_contest_submissions(
        self,
        contest_id: int,
    ) -> list[Submission]:
        

        statement = (
            select(Submission)
            .where(
                Submission.contest_id == contest_id,
            )
            .options(
                joinedload(Submission.user),
                joinedload(Submission.problem),
            )
            .order_by(
                Submission.user_id,
                Submission.problem_id,
                Submission.created_at,
            )
        )

        return list(
            self.db.scalars(statement).all()
        )
    
    def get_submissions_grouped_by_user(
        self,
        contest_id: int,
    ) -> dict[int, list[Submission]]:

        submissions = self.get_contest_submissions(
            contest_id
        )

        grouped: dict[int, list[Submission]] = (
            defaultdict(list)
        )

        for submission in submissions:
            grouped[submission.user_id].append(
                submission
            )

        return dict(grouped)
    
    def get_submissions_grouped_by_problem(
        self,
        contest_id: int,
    ) -> dict[int, list[Submission]]:
        

        submissions = self.get_contest_submissions(
            contest_id
        )

        grouped: dict[int, list[Submission]] = (
            defaultdict(list)
        )

        for submission in submissions:
            grouped[submission.problem_id].append(
                submission
            )

        return dict(grouped)
    
    def get_accepted_submissions(
        self,
        contest_id: int,
    ) -> list[Submission]:

        statement = (
            select(Submission)
            .where(
                Submission.contest_id == contest_id,
                Submission.verdict
                == SubmissionVerdict.ACCEPTED,
            )
            .options(
                joinedload(Submission.user),
                joinedload(Submission.problem),
            )
            .order_by(
                Submission.user_id,
                Submission.problem_id,
                Submission.created_at,
            )
        )

        return list(
            self.db.scalars(statement).all()
        )
    
