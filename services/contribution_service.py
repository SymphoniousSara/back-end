from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from decimal import Decimal

from models.contributions import Contribution
from repositories.contribution_repository import ContributionRepository
from repositories.birthday_repository import BirthdayRepository
from schemas.contributions import ContributionCreateSchema, ContributionUpdateSchema


class ContributionService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = ContributionRepository(db)
        self.birthday_repository = BirthdayRepository(db)

    def add_contribution(
            self,
            contributor_id: UUID,
            contribution_data: ContributionCreateSchema
    ) -> Contribution:

        birthday_id = contribution_data.birthday_id

        # Verify birthday exists
        birthday = self.birthday_repository.get_by_id(birthday_id)
        if not birthday:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Birthday not found"
            )

        # Can't contribute to own birthday
        if birthday.user_id == contributor_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot contribute to your own birthday"
            )

        # Check if already contributed
        if self.repository.contribution_exists(birthday_id, contributor_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already signed up to contribute to this birthday"
            )

        # Create contribution with initial amount (will be updated later)
        contribution = self.repository.create(
            birthday_id=birthday_id,
            contributor_id=contributor_id,
            #amount=Decimal('0'),
            paid=False
        )

        return contribution

    def get_birthday_contributions(
            self,
            birthday_id: UUID,
            current_user_id: UUID
    ) -> list[type[Contribution]]:

        birthday = self.birthday_repository.get_by_id(birthday_id)
        if not birthday:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Birthday not found"
            )

        return self.repository.get_by_birthday_id(birthday_id)


    # Get all contributions made by a user.
    def get_user_contributions(
            self,
            user_id: UUID
    ) -> List[Contribution]:

        return self.repository.get_by_contributor_id(user_id)

    def update_contribution(
            self,
            contribution_id: UUID,
            current_user_id: UUID,
            update_data: ContributionUpdateSchema
    ) -> Contribution:
        # Update contribution (amount or payment status).
        contribution = self.repository.get_by_id(contribution_id)
        if not contribution:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contribution not found"
            )

        birthday = self.birthday_repository.get_by_id(contribution.birthday_id)

        # Only organizer or the contributor can update
        is_organizer = birthday.organizer_id == current_user_id
        is_contributor = contribution.contributor_id == current_user_id

        if not (is_organizer or is_contributor):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own contributions or if you're the organizer"
            )

        # Organizer can update amount for all contributors
        # Contributor can only update their own paid status
        update_dict = {}

        if is_organizer:
            # Organizer can update both amount and paid status
            if update_data.amount is not None:
                update_dict['amount'] = update_data.amount
            if update_data.paid is not None:
                update_dict['paid'] = update_data.paid
        elif is_contributor:
            # Contributor can only update their paid status
            if update_data.paid is not None:
                update_dict['paid'] = update_data.paid

        if not update_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid fields to update"
            )

        updated_contribution = self.repository.update(contribution_id, **update_dict)
        return updated_contribution

    def remove_contribution(
            self,
            contribution_id: UUID,
            current_user_id: UUID
    ) -> bool:

        contribution = self.repository.get_by_id(contribution_id)
        if not contribution:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contribution not found"
            )

        # Only the contributor can remove their contribution
        if contribution.contributor_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only remove your own contributions"
            )

        success = self.repository.delete(contribution_id)
        return success

    # Can be retouched later?
    def calculate_equal_split(
            self,
            birthday_id: UUID,
            current_user_id: UUID
    ) -> dict:

        birthday = self.birthday_repository.get_by_id(birthday_id)
        if not birthday:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Birthday not found"
            )

        # Only organizer can calculate split
        if birthday.organizer_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the organizer can calculate contribution splits"
            )

        contributions = self.repository.get_by_birthday_id(birthday_id)

        if not contributions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No contributors yet"
            )

        total_amount = birthday.total_amount
        num_contributors = len(contributions)

        per_person = total_amount / num_contributors

        # Update each contribution with equal amount
        for contribution in contributions:
            self.repository.update(contribution.id, amount=per_person)

        return {
            "total_amount": total_amount,
            "num_contributors": num_contributors,
            "per_person_amount": per_person
        }

    def get_contribution_summary(self, birthday_id: UUID) -> dict:
        return self.repository.get_contribution_summary(birthday_id)