from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.submission import (
    SubmissionStatus,
    SubmissionVerdict,
)


class SubmissionCreate(BaseModel):

    language: str = Field(..., max_length=50)
    source_code: str = Field(..., min_length=1)


class SubmissionResponse(BaseModel):

    id: int

    user_id: int
    problem_id: int

    language: str
    source_code: str

    status: SubmissionStatus
    verdict: SubmissionVerdict | None

    execution_time_ms: int | None
    memory_used_kb: int | None

    compiler_output: str | None

    submitted_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class SubmissionListResponse(BaseModel):
  
    id: int

    user_id: int
    problem_id: int

    language: str

    status: SubmissionStatus
    verdict: SubmissionVerdict | None

    submitted_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class SubmissionStatusResponse(BaseModel):

    id: int

    status: SubmissionStatus
    verdict: SubmissionVerdict | None

    execution_time_ms: int | None
    memory_used_kb: int | None

    model_config = ConfigDict(
        from_attributes=True,
    )