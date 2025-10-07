from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.users import User
from repositories.user_repository import UserRepository
from schemas.users import UserCreateSchema, UserUpdateSchema
from core.utils import parse_name_from_email, validate_company_email


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)

    def create_user_from_email(
            self,
            user_data: UserCreateSchema
    ) -> User:
        email = user_data.email.lower()

        # Check if user already exists
        if self.repository.email_exists(email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        # Validate company email
        if not validate_company_email(email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email must be from company domain"
            )

        # Extract names from email
        first_name, last_name = parse_name_from_email(email)

        # Create user
        user = self.repository.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            birthday=user_data.birthday,
            role="user"
        )

        return user

    def get_or_create_user(self, email: str) -> User:
        pass