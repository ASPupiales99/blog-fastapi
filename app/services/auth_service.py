from fastapi import HTTPException, status

from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User, UserCreate
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register_user(self, user_data: UserCreate) -> User:
        if self.repo.get_user_by_email(user_data.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        new_user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            password=hash_password(user_data.password[:72])
        )

        return self.repo.create_user(new_user)

    def login(self, email: str, password: str) -> str:
        user = self.repo.get_user_by_email(email)
        if not user or not verify_password(password[:72], user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        return create_access_token({"sub": str(user.id)})
