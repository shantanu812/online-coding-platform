from sqlalchemy.orm import Session

from app.auth.hashing import hash_password, verify_password
from app.auth.jwt import create_access_token
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register_user(self, user_data: UserCreate) -> User:
       
        existing_user = self.repository.get_user_by_email(user_data.email)

        if existing_user:
            raise ValueError("Email is already registered.")

        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            password_hash=hash_password(user_data.password),
        )

        return self.repository.create_user(user)

    def authenticate_user(
        self,
        email: str,
        password: str,
    ) -> str | None:
        

        user = self.repository.get_user_by_email(email)

        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return create_access_token(subject=str(user.id))

    def get_user_by_id(
        self,
        user_id: int,
    ) -> User | None:
       

        return self.repository.get_user_by_id(user_id)

    def list_users(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[User]:
        

        return self.repository.list_users(skip, limit)

    def update_user(self, user: User) -> User:
        

        return self.repository.update_user(user)

    def delete_user(self, user: User) -> None:
        

        self.repository.delete_user(user)