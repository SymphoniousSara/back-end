from typing import List
from uuid import UUID
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from decimal import Decimal

from models.birthdays import Birthday
from models.users import User
from repositories.birthday_repository import BirthdayRepository
from repositories.user_repository import UserRepository
from repositories.contribution_repository import ContributionRepository
from schemas.birthdays import BirthdayCreateSchema, BirthdayUpdateSchema


class BirthdayService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = BirthdayRepository(db)
        self.user_repository = UserRepository(db)

    def create_birthday_entries(self) -> List[Birthday]:

        # Auto-create birthday entries for users with birthdays in next 2 months.
        # This should be called by a cron job or manually.

        today = date.today()
        current_year = today.year
        end_date = today + relativedelta(months=2)

        # Get all users with birthdays
        users = self.db.query(User).filter(User.birthday.isnot(None)).all()

        created_birthdays = []

        for user in users:
            if not user.birthday:
                continue

            # Calculate this year's birthday date
            birthday_this_year = date(
                current_year,
                user.birthday.month,
                user.birthday.day
            )

            # If birthday already passed, check next year
            if birthday_this_year < today:
                birthday_this_year = date(
                    current_year + 1,
                    user.birthday.month,
                    user.birthday.day
                )

            # Only create if within next 2 months
            if today <= birthday_this_year <= end_date:
                # Check if entry already exists
                existing = self.repository.get_by_user_and_year(
                    user.id,
                    birthday_this_year.year
                )

                if not existing:
                    birthday = self.repository.create(
                        user_id=user.id,
                        organizer_id=user.id,  # Placeholder, will be updated
                        date_year=birthday_this_year,
                        gift_description="",
                        total_amount=Decimal('0')
                    )
                    created_birthdays.append(birthday)

        return created_birthdays

    def get_upcoming_birthdays(
            self,
            current_user_id: UUID,
            months_ahead: int = 2
    ) -> list[type[Birthday]]:

        return self.repository.get_upcoming_birthdays(
            months_ahead=months_ahead,
            include_relations=True
        )

    def get_birthday_details(
            self,
            birthday_id: UUID,
            current_user_id: UUID
    ) -> Birthday:

        # Get birthday details with appropriate visibility based on user role.

        birthday = self.repository.get_all_contributions(birthday_id)
        if not birthday:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Birthday not found"
            )

        return birthday

    def assign_organizer_and_details(
            self,
            birthday_id: UUID,
            organizer_id: UUID,
            update_data: BirthdayUpdateSchema
    ) -> Birthday:

        # Assign organizer and update gift details for a birthday.
        # Only organizer can update these fields.

        birthday = self.repository.get_by_id(birthday_id)
        if not birthday:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Birthday not found"
            )

        # Can't organize own birthday
        if birthday.user_id == organizer_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot organize your own birthday"
            )

        # Prepare update data
        update_dict = update_data.model_dump(exclude_unset=True)
        update_dict['organizer_id'] = organizer_id

        # Update birthday
        updated_birthday = self.repository.update(birthday_id, **update_dict)

        return updated_birthday

    def update_birthday(
            self,
            birthday_id: UUID,
            current_user_id: UUID,
            update_data: BirthdayUpdateSchema
    ) -> Birthday:

        # Update birthday details (organizer only).

        birthday = self.repository.get_by_id(birthday_id)
        if not birthday:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Birthday not found"
            )

        # Only organizer can update
        if birthday.organizer_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the organizer can update birthday details"
            )

        update_dict = update_data.model_dump(exclude_unset=True)
        updated_birthday = self.repository.update(birthday_id, **update_dict)

        return updated_birthday

    def get_birthdays_organized_by_user(
            self,
            organizer_id: UUID
    ) -> list[type[Birthday]]:

        # Get all birthdays organized by a specific user.

        return self.repository.get_organized_by_user(organizer_id)

    def is_user_organizer(
            self,
            birthday_id: UUID,
            user_id: UUID
    ) -> bool:

        birthday = self.repository.get_by_id(birthday_id)
        return birthday and birthday.organizer_id == user_id

    def is_user_contributor(
            self,
            birthday_id: UUID,
            user_id: UUID
    ) -> bool:
        contrib_repo = ContributionRepository(self.db)
        return contrib_repo.contribution_exists(birthday_id, user_id)