from datetime import datetime, timezone

from app.models.contest import Contest
from app.repositories.contest_repository import ContestRepository
from app.schemas.contest import (
    ContestCreate,
    ContestUpdate,
)


class ContestService:
    

    def __init__(
        self,
        repository: ContestRepository,
    ):
        self.repository = repository

    def create_contest(
        self,
        contest_data: ContestCreate,
        created_by: int,
    ) -> Contest:

        self._validate_dates(
            contest_data.start_time,
            contest_data.end_time,
        )

        self._validate_overlap(
            contest_data.start_time,
            contest_data.end_time,
        )

        contest = Contest(
            **contest_data.model_dump(),
            created_by=created_by,
        )

        return self.repository.create_contest(contest)

    def update_contest(
        self,
        contest_id: int,
        contest_data: ContestUpdate,
    ) -> Contest:

        contest = self._get_contest(contest_id)

        data = contest_data.model_dump(
            exclude_unset=True
        )

        start = data.get(
            "start_time",
            contest.start_time,
        )

        end = data.get(
            "end_time",
            contest.end_time,
        )

        self._validate_dates(start, end)
        self._validate_overlap(
            start,
            end,
            exclude_id=contest.id,
        )

        for key, value in data.items():
            setattr(contest, key, value)

        return self.repository.update_contest(
            contest
        )

    def delete_contest(
        self,
        contest_id: int,
    ) -> None:

        contest = self._get_contest(contest_id)

        self.repository.delete_contest(contest)

    def get_contest(
        self,
        contest_id: int,
    ) -> Contest:
        return self._get_contest(contest_id)

    def list_contests(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Contest]:
        return self.repository.list_contests(
            skip,
            limit,
        )

    def register_user(
        self,
        contest_id: int,
        user_id: int,
    ) -> None:

        contest = self._get_contest(contest_id)

        if contest.start_time <= datetime.now(timezone.utc):
            raise ValueError(
                "Registration is closed."
            )

        if self.repository.is_user_registered(
            contest_id,
            user_id,
        ):
            raise ValueError(
                "User already registered."
            )

        self.repository.register_participant(
            contest_id,
            user_id,
        )

    def add_problem(
        self,
        contest_id: int,
        problem_id: int,
    ) -> None:

        self._get_contest(contest_id)

        if self.repository.is_problem_added(
            contest_id,
            problem_id,
        ):
            raise ValueError(
                "Problem already added."
            )

        self.repository.add_problem(
            contest_id,
            problem_id,
        )

    def remove_problem(
        self,
        contest_id: int,
        problem_id: int,
    ) -> None:

        self._get_contest(contest_id)

        self.repository.remove_problem(
            contest_id,
            problem_id,
        )

    def get_contest_problems(
        self,
        contest_id: int,
    ):
        self._get_contest(contest_id)

        return self.repository.get_contest_problems(
            contest_id
        )

    def get_contest_participants(
        self,
        contest_id: int,
    ):
        self._get_contest(contest_id)

        return self.repository.get_contest_participants(
            contest_id
        )

    def get_contests_by_status(
        self,
        status: str,
    ):
        return self.repository.get_contests_by_status(
            status
        )

    @staticmethod
    def calculate_status(
        contest: Contest,
    ) -> str:

        now = datetime.now(timezone.utc)

        if now < contest.start_time:
            return "UPCOMING"

        if now > contest.end_time:
            return "FINISHED"

        return "RUNNING"

    @staticmethod
    def _validate_dates(
        start_time,
        end_time,
    ):

        if end_time <= start_time:
            raise ValueError(
                "End time must be after start time."
            )

    def _validate_overlap(
        self,
        start_time,
        end_time,
        exclude_id: int | None = None,
    ):

        contests = self.repository.list_contests()

        for contest in contests:

            if (
                exclude_id
                and contest.id == exclude_id
            ):
                continue

            if (
                start_time < contest.end_time
                and end_time > contest.start_time
            ):
                raise ValueError(
                    "Contest overlaps with an existing contest."
                )

    def _get_contest(
        self,
        contest_id: int,
    ) -> Contest:

        contest = self.repository.get_contest_by_id(
            contest_id
        )

        if contest is None:
            raise ValueError(
                "Contest not found."
            )

        return contest