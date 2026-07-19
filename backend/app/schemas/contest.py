from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.contest import ContestVisibility


class ContestBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: str | None = None

    visibility: ContestVisibility = ContestVisibility.PUBLIC

    start_time: datetime
    end_time: datetime

    duration_minutes: int = Field(..., gt=0)



class ContestCreate(ContestBase):
    pass


class ContestUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=255)
    description: str | None = None

    visibility: ContestVisibility | None = None

    start_time: datetime | None = None
    end_time: datetime | None = None

    duration_minutes: int | None = Field(
        default=None,
        gt=0,
    )


    is_active: bool | None = None


class ContestProblemAdd(BaseModel):
    problem_id: int


class ContestRegistration(BaseModel):
    contest_id: int


class ContestResponse(BaseModel):
    id: int

    title: str
    description: str | None

    visibility: ContestVisibility

    start_time: datetime
    end_time: datetime

    duration_minutes: int

    is_active: bool

    created_by: int

    created_at: datetime
    updated_at: datetime

    status: str

    model_config = ConfigDict(
        from_attributes=True,
    )


class ContestListResponse(BaseModel):
    contests: list[ContestResponse]
    total: int