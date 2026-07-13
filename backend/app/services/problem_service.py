from app.models.problem import Problem
from app.repositories.problem_repository import ProblemRepository
from app.schemas.problem import ProblemCreate, ProblemUpdate


class ProblemService:
    
    def __init__(self, repository: ProblemRepository):
        self.repository = repository

    def create_problem(
        self,
        problem_data: ProblemCreate,
        created_by: int,
    ) -> Problem:
        

        existing_problem = self.repository.get_problem_by_slug(
            problem_data.slug
        )

        if existing_problem:
            raise ValueError("A problem with this slug already exists.")

        problem = Problem(
            title=problem_data.title,
            slug=problem_data.slug,
            statement=problem_data.statement,
            difficulty=problem_data.difficulty,
            time_limit_ms=problem_data.time_limit_ms,
            memory_limit_mb=problem_data.memory_limit_mb,
            input_format=problem_data.input_format,
            output_format=problem_data.output_format,
            constraints=problem_data.constraints,
            sample_input=problem_data.sample_input,
            sample_output=problem_data.sample_output,
            explanation=problem_data.explanation,
            is_public=problem_data.is_public,
            created_by=created_by,
        )

        return self.repository.create_problem(problem)

    def get_problem(
        self,
        problem_id: int,
    ) -> Problem:
        

        problem = self.repository.get_problem_by_id(problem_id)

        if problem is None:
            raise ValueError("Problem not found.")

        return problem

    def get_problem_by_slug(
        self,
        slug: str,
    ) -> Problem:
        
        problem = self.repository.get_problem_by_slug(slug)

        if problem is None:
            raise ValueError("Problem not found.")

        return problem

    def list_problems(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Problem]:
       

        return self.repository.list_problems(skip, limit)

    def update_problem(
        self,
        problem_id: int,
        problem_data: ProblemUpdate,
    ) -> Problem:
      
        problem = self.repository.get_problem_by_id(problem_id)

        if problem is None:
            raise ValueError("Problem not found.")

        if (
            problem_data.slug is not None
            and problem_data.slug != problem.slug
        ):
            existing_problem = self.repository.get_problem_by_slug(
                problem_data.slug
            )

            if existing_problem:
                raise ValueError(
                    "A problem with this slug already exists."
                )

        update_data = problem_data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        for field, value in update_data.items():
            setattr(problem, field, value)

        return self.repository.update_problem(problem)

    def delete_problem(
        self,
        problem_id: int,
    ) -> None:
        

        problem = self.repository.get_problem_by_id(problem_id)

        if problem is None:
            raise ValueError("Problem not found.")

        self.repository.delete_problem(problem)