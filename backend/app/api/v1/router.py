from fastapi import APIRouter
from app.api.v1.judge import router as judge_router
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.problems import router as problems_router
from app.api.v1.test_cases import router as test_case_router
from app.api.v1.submissions import router as submissions_router
api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(problems_router)
api_router.include_router(submissions_router)
api_router.include_router(test_case_router)
api_router.include_router(judge_router)