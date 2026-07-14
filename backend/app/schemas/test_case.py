from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TestCaseBase(BaseModel):

    input: str
    expected_output: str

    is_sample: bool = False
    is_hidden: bool = True


class TestCaseCreate(TestCaseBase):

    pass


class TestCaseUpdate(BaseModel):

    input: str | None = None
    expected_output: str | None = None

    is_sample: bool | None = None
    is_hidden: bool | None = None


class TestCaseResponse(TestCaseBase):

    id: int
    problem_id: int

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TestCaseListResponse(BaseModel):
   

    id: int

    problem_id: int

    is_sample: bool
    is_hidden: bool

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SampleTestCaseResponse(BaseModel):
  
    id: int

    input: str
    expected_output: str

    model_config = ConfigDict(from_attributes=True)