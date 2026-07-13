from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.problem import Difficulty


class ProblemBase(BaseModel):
  
    title: str = Field(..., max_length=255)
    slug: str = Field(..., max_length=255)

    statement: str

    difficulty: Difficulty

    time_limit_ms: int = Field(default=1000, ge=1)
    memory_limit_mb: int = Field(default=256, ge=1)

    input_format: str
    output_format: str
    constraints: str

    sample_input: str
    sample_output: str

    explanation: str | None = None

    is_public: bool = False


class ProblemCreate(ProblemBase):

    pass


class ProblemUpdate(BaseModel):

    title: str | None = Field(default=None, max_length=255)
    slug: str | None = Field(default=None, max_length=255)

    statement: str | None = None

    difficulty: Difficulty | None = None

    time_limit_ms: int | None = Field(default=None, ge=1)
    memory_limit_mb: int | None = Field(default=None, ge=1)

    input_format: str | None = None
    output_format: str | None = None
    constraints: str | None = None

    sample_input: str | None = None
    sample_output: str | None = None

    explanation: str | None = None

    is_public: bool | None = None


class ProblemResponse(ProblemBase):
    
    id: int

    created_by: int

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProblemListResponse(BaseModel):

    id: int

    title: str
    slug: str

    difficulty: Difficulty

    time_limit_ms: int
    memory_limit_mb: int

    is_public: bool

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)