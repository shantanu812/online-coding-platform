from app.models.test_case import TestCase
from app.repositories.problem_repository import ProblemRepository
from app.repositories.test_case_repository import TestCaseRepository
from app.schemas.test_case import (
    TestCaseCreate,
    TestCaseUpdate,
)


class TestCaseService:

    def __init__(
        self,
        test_case_repository: TestCaseRepository,
        problem_repository: ProblemRepository,
    ):
        self.test_case_repository = test_case_repository
        self.problem_repository = problem_repository

    def create_test_case(
        self,
        problem_id: int,
        test_case_data: TestCaseCreate,
    ) -> TestCase:
        

        problem = self.problem_repository.get_problem_by_id(problem_id)

        if problem is None:
            raise ValueError("Problem not found.")

        if (
            test_case_data.is_sample
            and test_case_data.is_hidden
        ):
            raise ValueError(
                "A test case cannot be both sample and hidden."
            )

        existing_test_cases = (
            self.test_case_repository.get_test_cases_by_problem(
                problem_id
            )
        )

        for test_case in existing_test_cases:
            if (
                test_case.is_sample
                and test_case.input == test_case_data.input
                and test_case.expected_output
                == test_case_data.expected_output
            ):
                raise ValueError(
                    "Duplicate sample test case."
                )

        new_test_case = TestCase(
            problem_id=problem_id,
            input=test_case_data.input,
            expected_output=test_case_data.expected_output,
            is_sample=test_case_data.is_sample,
            is_hidden=test_case_data.is_hidden,
        )

        return self.test_case_repository.create_test_case(
            new_test_case
        )

    def get_test_case(
        self,
        test_case_id: int,
    ) -> TestCase:
        

        test_case = (
            self.test_case_repository.get_test_case_by_id(
                test_case_id
            )
        )

        if test_case is None:
            raise ValueError("Test case not found.")

        return test_case

    def get_test_cases_by_problem(
        self,
        problem_id: int,
        samples_only: bool = False,
    ) -> list[TestCase]:
       
        problem = self.problem_repository.get_problem_by_id(
            problem_id
        )

        if problem is None:
            raise ValueError("Problem not found.")

        test_cases = (
            self.test_case_repository.get_test_cases_by_problem(
                problem_id
            )
        )

        if samples_only:
            return self.test_case_repository.get_sample_test_cases_by_problem(
                problem_id
            )

        return test_cases

    def list_test_cases(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[TestCase]:
       

        return self.test_case_repository.list_test_cases(
            skip,
            limit,
        )

    def update_test_case(
        self,
        test_case_id: int,
        test_case_data: TestCaseUpdate,
    ) -> TestCase:
       

        test_case = (
            self.test_case_repository.get_test_case_by_id(
                test_case_id
            )
        )

        if test_case is None:
            raise ValueError("Test case not found.")

        update_data = test_case_data.model_dump(
            exclude_unset=True
        )

        new_is_sample = update_data.get(
            "is_sample",
            test_case.is_sample,
        )

        new_is_hidden = update_data.get(
            "is_hidden",
            test_case.is_hidden,
        )

        if new_is_sample and new_is_hidden:
            raise ValueError(
                "A test case cannot be both sample and hidden."
            )

        for field, value in update_data.items():
            setattr(test_case, field, value)

        return self.test_case_repository.update_test_case(
            test_case
        )

    def delete_test_case(
        self,
        test_case_id: int,
    ) -> None:
        
        test_case = (
            self.test_case_repository.get_test_case_by_id(
                test_case_id
            )
        )

        if test_case is None:
            raise ValueError("Test case not found.")

        self.test_case_repository.delete_test_case(
            test_case
        )