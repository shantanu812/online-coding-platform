from sqlalchemy import select 
from sqlalchemy.orm import Session 

from app.models.test_case import TestCase


class TestCaseRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_test_case(
        self,
        test_case: TestCase,
    ) -> TestCase:
       
        self.db.add(test_case)
        self.db.commit()
        self.db.refresh(test_case)

        return test_case

    def get_test_case_by_id(
        self,
        test_case_id: int,
    ) -> TestCase | None:
        
        statement = select(TestCase).where(
            TestCase.id == test_case_id
        )

        return self.db.scalar(statement)

    def get_test_cases_by_problem(
        self,
        problem_id: int,
    ) -> list[TestCase]:
       
        statement = (
            select(TestCase)
            .where(TestCase.problem_id == problem_id)
            .order_by(TestCase.id)
        )

        return list(self.db.scalars(statement).all())

    def list_test_cases(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[TestCase]:
        
        statement = (
            select(TestCase)
            .offset(skip)
            .limit(limit)
        )

        return list(self.db.scalars(statement).all())

    def update_test_case(
        self,
        test_case: TestCase,
    ) -> TestCase:
        
        self.db.commit()
        self.db.refresh(test_case)

        return test_case

    def delete_test_case(
        self,
        test_case: TestCase,
    ) -> None:
        
        self.db.delete(test_case)
        self.db.commit()
    
    def get_sample_test_cases_by_problem(
        self,
        problem_id: int,
    ) -> list[TestCase]:
        statement = (
            select(TestCase)
            .where(
                TestCase.problem_id == problem_id,
                TestCase.is_sample.is_(True),
            )
            .order_by(TestCase.id)
        )

        return list(self.db.scalars(statement).all())
    
    def get_hidden_test_cases_by_problem(
        self,
        problem_id: int,
    ) -> list[TestCase]:
       
        statement = (
            select(TestCase)
            .where(
                TestCase.problem_id == problem_id,
                TestCase.is_hidden.is_(True),
            )
            .order_by(TestCase.id)
        )

        return list(
            self.db.scalars(statement).all()
        )