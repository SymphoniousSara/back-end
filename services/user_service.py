from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.users import User
from repositories.user_repository import UserRepository
from schemas.users import UserCreateSchema, UserUpdateSchema, UserPublicSchema
from core.utils import parse_name_from_email, validate_company_email


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)

    def get_or_create_user_from_email(self, email: str) -> User:
        """OAuth flow: Get existing user or create new one"""
        email = email.lower().strip()

        # Check if user already exists
        existing_user = self.repository.get_by_email(email)
        if existing_user:
            return existing_user

        # Optional: Validate company email (if you want this restriction)
        if not validate_company_email(email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email must be from company domain"
            )

        # Extract names from email
        first_name, last_name = parse_name_from_email(email)

        # Create new user
        user = self.repository.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role="user"
            # birth_date, nickname, bank_details are None by default
        )

        return user

    def get_user_by_id(self, user_id: UUID) -> User:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.repository.get_by_email(email.lower().strip())

    def update_profile(self, user_id: UUID, update_data: UserUpdateSchema) -> User:
        # Verify user exists first
        existing_user = self.get_user_by_id(user_id)

        update_dict = update_data.model_dump(exclude_unset=True)
        user = self.repository.update(user_id, **update_dict)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found after update"
            )

        return user

    def get_all_users(self) -> List[User]:
        return self.repository.get_all()

    def get_all_users_except(self, exclude_user_id: UUID) -> List[User]:
        return self.repository.get_all_except(exclude_user_id)

    def get_user_public_info(self, user_id: UUID) -> UserPublicSchema:
        user = self.get_user_by_id(user_id)
        return UserPublicSchema.model_validate(user)

    def get_users_with_upcoming_birthdays(self, days_ahead: int = 30) -> List[User]:
        from datetime import date, timedelta
        start_date = date.today()
        end_date = start_date + timedelta(days=days_ahead)

        return self.repository.get_users_with_birthdays_in_range(start_date, end_date)

    def email_exists(self, email: str) -> bool:
        return self.repository.email_exists(email.lower().strip())