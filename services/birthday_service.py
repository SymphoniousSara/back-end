from typing import List
from uuid import UUID
from datetime import date
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.birthdays import Birthday
from models.users import User
from repositories.birthday_repository import BirthdayRepository
from repositories.user_repository import UserRepository
from repositories.contribution_repository import ContributionRepository
from schemas.birthdays import BirthdayUpdateSchema


class BirthdayService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = BirthdayRepository(db)
        self.user_repository = UserRepository(db)
        self.contribution_repository = ContributionRepository(db)

    def create_birthday_entries(self) -> List[Birthday]:
        # Auto-create birthday entries for users with birthdays in next 2 months
        today = date.today()
        current_year = today.year
        end_date = today + relativedelta(months=2)

        users = self.db.query(User).filter(User.birth_date.isnot(None)).all()
        created_birthdays = []

        for user in users:
            if not user.birth_date:
                continue

            # Calculate this year's birthday date
            birthday_this_year = date(
                current_year,
                user.birth_date.month,
                user.birth_date.day
            )

            # If birthday already passed, check next year
            if birthday_this_year < today:
                birthday_this_year = date(
                    current_year + 1,
                    user.birth_date.month,
                    user.birth_date.day
                )

            # Only create if within next 2 months
            if today <= birthday_this_year <= end_date:
                # Check if entry already exists
                existing = self.repository.get_by_celebrant_and_year(
                    user.id,
                    birthday_this_year.year
                )

                if not existing:
                    birthday = self.repository.create(
                        celebrant_id=user.id,
                        celebration_date=birthday_this_year,
                        gift_description="",
                        total_amount=None,
                        organizer_id=None
                    )
                    created_birthdays.append(birthday)

        return created_birthdays

    def get_upcoming_birthdays(
            self,
            current_user_id: UUID,
            months_ahead: int = 2
    ) -> List[Birthday]:
        return self.repository.get_upcoming_birthdays(
            months_ahead=months_ahead,
            include_relations=True
        )

    def get_birthday_details(
            self,
            birthday_id: UUID,
            current_user_id: UUID
    ) -> Birthday:
        birthday = self.repository.get_with_contributions(birthday_id)
        if not birthday:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Birthday not found"
            )
        return birthday

    def become_organizer(
            self,
            birthday_id: UUID,
            organizer_id: UUID,
            update_data: BirthdayUpdateSchema
    ) -> Birthday:
        birthday = self.repository.get_by_id(birthday_id)
        if not birthday:
            raise HTTPException(404, "Birthday not found")

        # Can't organize own birthday
        if birthday.celebrant_id == organizer_id:
            raise HTTPException(400, "You cannot organize your own birthday")

        # Check if already has organizer
        if birthday.organizer_id is not None:
            raise HTTPException(400, "Birthday already has an organizer")

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
        birthday = self.repository.get_by_id(birthday_id)
        if not birthday:
            raise HTTPException(404, "Birthday not found")

        # Only organizer can update
        if birthday.organizer_id != current_user_id:
            raise HTTPException(403, "Only the organizer can update birthday details")

        update_dict = update_data.model_dump(exclude_unset=True)
        updated_birthday = self.repository.update(birthday_id, **update_dict)
        return updated_birthday

    def calculate_contribution_amounts(
            self,
            birthday_id: UUID,
            current_user_id: UUID
    ) -> Birthday:
        birthday = self.repository.get_by_id(birthday_id)
        if not birthday:
            raise HTTPException(404, "Birthday not found")

        # Only organizer can calculate
        if birthday.organizer_id != current_user_id:
            raise HTTPException(403, "Only organizer can calculate amounts")

        if not birthday.total_amount:
            raise HTTPException(400, "Total amount must be set first")

        contributions = self.contribution_repository.get_by_birthday_id(birthday_id)

        if not contributions:
            raise HTTPException(400, "No contributors yet")

        # Calculate equal split (integer division for MKD)
        total_amount = birthday.total_amount
        num_contributors = len(contributions)
        per_person_amount = total_amount // num_contributors

        # Update all contributions with calculated amount
        for contribution in contributions:
            self.contribution_repository.update(
                contribution.id,
                amount=per_person_amount
            )

        return birthday

    def get_birthdays_organized_by_user(
            self,
            organizer_id: UUID
    ) -> List[Birthday]:
        return self.repository.get_organized_by_user(organizer_id)

    def get_birthdays_for_celebrant(
            self,
            celebrant_id: UUID
    ) -> List[Birthday]:
        return self.repository.get_birthdays_for_celebrant(celebrant_id)

    def get_birthdays_without_organizer(self) -> List[Birthday]:
        return self.repository.get_birthdays_without_organizer()

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
        return self.contribution_repository.contribution_exists(birthday_id, user_id)