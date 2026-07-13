from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.problem import Problem


class ProblemRepository:
    
    def __init__(self, db: Session):
        self.db = db

    def create_problem(self, problem: Problem) -> Problem:
        
        self.db.add(problem)
        self.db.commit()
        self.db.refresh(problem)

        return problem

    def get_problem_by_id(self, problem_id: int) -> Problem | None:
       
        statement = select(Problem).where(
            Problem.id == problem_id
        )

        return self.db.scalar(statement)

    def get_problem_by_slug(self, slug: str) -> Problem | None:
       
        statement = select(Problem).where(
            Problem.slug == slug
        )

        return self.db.scalar(statement)

    def list_problems(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Problem]:
        
        statement = (
            select(Problem)
            .offset(skip)
            .limit(limit)
        )

        return list(self.db.scalars(statement).all())

    def update_problem(self, problem: Problem) -> Problem:
        
        self.db.commit()
        self.db.refresh(problem)

        return problem

    def delete_problem(self, problem: Problem) -> None:
        
        self.db.delete(problem)
        self.db.commit()