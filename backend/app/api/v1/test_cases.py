from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)

from app.api.dependencies import (
    get_current_active_user,
    get_current_admin_user,
    get_test_case_service,
)
from app.models.user import User
from app.schemas.test_case import (
    SampleTestCaseResponse,
    TestCaseCreate,
    TestCaseListResponse,
    TestCaseResponse,
    TestCaseUpdate,
)
from app.services.test_case_service import TestCaseService

router = APIRouter(
    tags=["Test Cases"],
)

@router.post(
    "/problems/{problem_id}/test-cases",
    response_model=TestCaseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_test_case(
    problem_id: int,
    test_case_data: TestCaseCreate,
    _: User = Depends(get_current_admin_user),
    service: TestCaseService = Depends(get_test_case_service),
):
    try:
        return service.create_test_case(
            problem_id,
            test_case_data,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@router.get(
    "/test-cases/{test_case_id}",
    response_model=TestCaseResponse,
)
def get_test_case(
    test_case_id: int,
    _: User = Depends(get_current_admin_user),
    service: TestCaseService = Depends(get_test_case_service),
):
    try:
        return service.get_test_case(test_case_id)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    
@router.put(
    "/test-cases/{test_case_id}",
    response_model=TestCaseResponse,
)
def update_test_case(
    test_case_id: int,
    test_case_data: TestCaseUpdate,
    _: User = Depends(get_current_admin_user),
    service: TestCaseService = Depends(get_test_case_service),
):
    try:
        return service.update_test_case(
            test_case_id,
            test_case_data,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@router.delete(
    "/test-cases/{test_case_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_test_case(
    test_case_id: int,
    _: User = Depends(get_current_admin_user),
    service: TestCaseService = Depends(get_test_case_service),
):
    try:
        service.delete_test_case(test_case_id)

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

@router.get(
    "/problems/{problem_id}/samples",
    response_model=list[SampleTestCaseResponse],
)
def get_sample_test_cases(
    problem_id: int,
    _: User = Depends(get_current_active_user),
    service: TestCaseService = Depends(get_test_case_service),
):
    try:
        return service.get_test_cases_by_problem(
            problem_id,
            samples_only=True,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )