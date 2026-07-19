from datetime import datetime, timezone

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.contest import (
    Contest,
    contest_participants,
    contest_problems,
)
from app.models.problem import Problem
from app.models.user import User


class ContestRepository:
   
    def __init__(self, db: Session):
        self.db = db

    def create_contest(
        self,
        contest: Contest,
    ) -> Contest:
        self.db.add(contest)
        self.db.commit()
        self.db.refresh(contest)
        return contest

    def update_contest(
        self,
        contest: Contest,
    ) -> Contest:
        self.db.commit()
        self.db.refresh(contest)
        return contest

    def delete_contest(
        self,
        contest: Contest,
    ) -> None:
        self.db.delete(contest)
        self.db.commit()

    def get_contest_by_id(
        self,
        contest_id: int,
    ) -> Contest | None:
        statement = select(Contest).where(
            Contest.id == contest_id
        )

        return self.db.scalar(statement)

    def list_contests(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Contest]:
        statement = (
            select(Contest)
            .offset(skip)
            .limit(limit)
            .order_by(Contest.start_time)
        )

        return list(self.db.scalars(statement).all())

    def register_participant(
        self,
        contest_id: int,
        user_id: int,
    ) -> None:
        self.db.execute(
            contest_participants.insert().values(
                contest_id=contest_id,
                user_id=user_id,
            )
        )

        self.db.commit()

    def add_problem(
        self,
        contest_id: int,
        problem_id: int,
    ) -> None:
        self.db.execute(
            contest_problems.insert().values(
                contest_id=contest_id,
                problem_id=problem_id,
            )
        )

        self.db.commit()

    def remove_problem(
        self,
        contest_id: int,
        problem_id: int,
    ) -> None:
        self.db.execute(
            delete(contest_problems).where(
                contest_problems.c.contest_id == contest_id,
                contest_problems.c.problem_id == problem_id,
            )
        )

        self.db.commit()

    def get_contest_problems(
        self,
        contest_id: int,
    ) -> list[Problem]:
        contest = self.get_contest_by_id(contest_id)

        return contest.problems if contest else []

    def get_contest_participants(
        self,
        contest_id: int,
    ) -> list[User]:
        contest = self.get_contest_by_id(contest_id)

        return contest.participants if contest else []

    def get_contests_by_status(
        self,
        status: str,
    ) -> list[Contest]:
        now = datetime.now(timezone.utc)

        if status.upper() == "UPCOMING":
            statement = select(Contest).where(
                Contest.start_time > now
            )

        elif status.upper() == "RUNNING":
            statement = select(Contest).where(
                Contest.start_time <= now,
                Contest.end_time >= now,
            )

        elif status.upper() == "FINISHED":
            statement = select(Contest).where(
                Contest.end_time < now
            )

        else:
            return []

        return list(self.db.scalars(statement).all())

    def is_user_registered(
        self,
        contest_id: int,
        user_id: int,
    ) -> bool:
        statement = (
            select(contest_participants)
            .where(
                contest_participants.c.contest_id == contest_id,
                contest_participants.c.user_id == user_id,
            )
        )

        return self.db.execute(statement).first() is not None

    def is_problem_added(
        self,
        contest_id: int,
        problem_id: int,
    ) -> bool:
        statement = (
            select(contest_problems)
            .where(
                contest_problems.c.contest_id == contest_id,
                contest_problems.c.problem_id == problem_id,
            )
        )

        return self.db.execute(statement).first() is not None