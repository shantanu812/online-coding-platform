from pydantic import BaseModel, ConfigDict, Field


class ProblemScore(BaseModel):

    problem_id: int

    solved: bool

    score: int = Field(default=0, ge=0)

    penalty_minutes: int = Field(default=0, ge=0)

    accepted_submission_id: int | None = None

    accepted_at_minutes: int | None = None

    wrong_attempts: int = Field(default=0, ge=0)


class SubmissionStatistic(BaseModel):

    total_submissions: int = Field(ge=0)

    accepted_submissions: int = Field(ge=0)

    wrong_submissions: int = Field(ge=0)

    compilation_errors: int = Field(default=0, ge=0)

    runtime_errors: int = Field(default=0, ge=0)

    time_limit_exceeded: int = Field(default=0, ge=0)

    memory_limit_exceeded: int = Field(default=0, ge=0)


class LeaderboardEntry(BaseModel):

    rank: int

    user_id: int

    full_name: str

    total_score: int = Field(ge=0)

    solved_problems: int = Field(ge=0)

    total_penalty: int = Field(ge=0)

    last_accepted_time: int | None = None

    problem_scores: list[ProblemScore]

    statistics: SubmissionStatistic

    model_config = ConfigDict(
        from_attributes=True,
    )


class LeaderboardResponse(BaseModel):

    contest_id: int

    contest_title: str

    participant_count: int

    leaderboard: list[LeaderboardEntry]

    model_config = ConfigDict(
        from_attributes=True,
    )