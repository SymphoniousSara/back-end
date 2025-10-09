from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID

from db.database import get_db
from core.dependencies import get_current_user_id
from schemas.contributions import (
    ContributionCreateSchema,
    ContributionUpdateSchema,
    ContributionResponseSchema,
    ContributionWithContributorSchema
)
from services.contribution_service import ContributionService

router = APIRouter(prefix="/contributions", tags=["Contributions"])


@router.post("", response_model=ContributionResponseSchema, status_code=status.HTTP_201_CREATED)
def contribute_to_birthday(
        contribution_data: ContributionCreateSchema,
        current_user_id: UUID = Depends(get_current_user_id),
        db: Session = Depends(get_db)
):
    """
    Sign up to contribute to a birthday.

    **Flow:**
    1. User clicks "I want to contribute" on a birthday card
    2. Entry is created in database with birthday_id and contributor_id
    3. Amount starts as NULL, will be calculated later by organizer
    4. Payment status defaults to False

    **Validation:**
    - Cannot contribute to own birthday
    - Cannot contribute twice to same birthday
    """
    service = ContributionService(db)
    contribution = service.add_contribution(current_user_id, contribution_data)
    return contribution


@router.get("/my", response_model=List[ContributionResponseSchema])
def get_my_contributions(
        current_user_id: UUID = Depends(get_current_user_id),
        db: Session = Depends(get_db)
):
    """
    Get all contributions made by current user.

    Shows:
    - Which birthdays user is contributing to
    - Amount they need to pay for each (once calculated by organizer)
    - Payment status
    """
    service = ContributionService(db)
    contributions = service.get_user_contributions(current_user_id)
    return contributions


@router.get("/birthday/{birthday_id}", response_model=List[ContributionWithContributorSchema])
def get_birthday_contributions(
        birthday_id: UUID,
        current_user_id: UUID = Depends(get_current_user_id),
        db: Session = Depends(get_db)
):
    """
    Get all contributors for a specific birthday.

    **Permissions:** Organizer or contributors of this birthday only

    Shows list of who is contributing with amounts and payment status.
    """
    service = ContributionService(db)
    contributions = service.get_birthday_contributions(birthday_id, current_user_id)
    return contributions


@router.put("/{contribution_id}", response_model=ContributionResponseSchema)
def update_contribution(
        contribution_id: UUID,
        update_data: ContributionUpdateSchema,
        current_user_id: UUID = Depends(get_current_user_id),
        db: Session = Depends(get_db)
):
    """
    Update contribution details.

    **Permissions:**
    - **Organizer:** Can update payment status for any contributor
    - **Contributor:** Can update their own paid status only

    **Note:** Amounts are calculated automatically via calculate-split, not manually updated

    **Use cases:**
    - Contributor marks as paid after transferring money
    - Organizer marks contributions as paid when confirmed
    """
    service = ContributionService(db)
    contribution = service.update_contribution(contribution_id, current_user_id, update_data)
    return contribution


@router.delete("/{contribution_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_contribution(
        contribution_id: UUID,
        current_user_id: UUID = Depends(get_current_user_id),
        db: Session = Depends(get_db)
):
    """
    Remove contribution (withdraw from birthday).

    **Permissions:** Contributor can only remove their own contributions
    """
    service = ContributionService(db)
    service.remove_contribution(contribution_id, current_user_id)
    return None


@router.get("/birthday/{birthday_id}/summary")
def get_contribution_summary(
        birthday_id: UUID,
        db: Session = Depends(get_db)
):
    """
    Get summary statistics for a birthday's contributions.

    Returns:
    - Total number of contributors
    - Total amount committed (once calculated)
    - Total amount paid
    - Total amount unpaid
    """
    service = ContributionService(db)
    summary = service.get_contribution_summary(birthday_id)
    return summary