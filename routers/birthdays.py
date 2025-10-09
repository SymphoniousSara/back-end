from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from uuid import UUID

from db.database import get_db
from core.dependencies import get_current_user_id
from schemas.birthdays import (
    BirthdayResponseSchema,
    BirthdayUpdateSchema,
    BirthdayWithContributionsSchema,
    BirthdayWithDetailsSchema
)
from services.birthday_service import BirthdayService

router = APIRouter(prefix="/birthdays", tags=["Birthdays"])


@router.get("", response_model=List[BirthdayWithDetailsSchema])
def list_upcoming_birthdays(
        months_ahead: int = Query(2, ge=1, le=6, description="Months to look ahead"),
        current_user_id: UUID = Depends(get_current_user_id),
        db: Session = Depends(get_db)
):
    """
    Returns birthdays with:
    - Celebrant info
    - Organizer info
    - Gift details
    - Basic celebration info
    """
    try:
        service = BirthdayService(db)
        birthdays = service.get_upcoming_birthdays(current_user_id, months_ahead)
        return birthdays
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise e


@router.get("/{birthday_id}", response_model=BirthdayWithContributionsSchema)
def get_birthday_details(
        birthday_id: UUID,
        current_user_id: UUID = Depends(get_current_user_id),
        db: Session = Depends(get_db)
):
    """
    Visibility depends on role:
    - Everyone: See basic info, gift idea, organizer
    - Contributor: See above + their own contribution details
    - Organizer: See everything + all contributions
    """
    service = BirthdayService(db)
    birthday = service.get_birthday_details(birthday_id, current_user_id)
    return birthday


@router.post("/{birthday_id}/organize", response_model=BirthdayResponseSchema)
def become_organizer(
        birthday_id: UUID,
        update_data: BirthdayUpdateSchema,
        current_user_id: UUID = Depends(get_current_user_id),
        db: Session = Depends(get_db)
):
    """
    Become organizer for a birthday and set initial details.

    One-time action:
    - Assigns current user as organizer
    - Sets gift description
    - Sets total amount
    - Cannot organize your own birthday

    Current logic does not involve another organizer.
    """
    service = BirthdayService(db)
    birthday = service.become_organizer(
        birthday_id,
        current_user_id,
        update_data
    )
    return birthday


@router.put("/{birthday_id}", response_model=BirthdayResponseSchema)
def update_birthday(
        birthday_id: UUID,
        update_data: BirthdayUpdateSchema,
        current_user_id: UUID = Depends(get_current_user_id),
        db: Session = Depends(get_db)
):
    """
    Organizer only - can update:
    - Gift description
    - Total amount
    - Celebration date

    Cannot change: celebrant, organizer
    """
    service = BirthdayService(db)
    birthday = service.update_birthday(birthday_id, current_user_id, update_data)
    return birthday


@router.post("/{birthday_id}/calculate-split", response_model=BirthdayResponseSchema)  # ✅ ADDED: From contributions
def calculate_contribution_split(
        birthday_id: UUID,
        current_user_id: UUID = Depends(get_current_user_id),
        db: Session = Depends(get_db)
):
    """
    Calculate equal split of total amount among contributors.
    Organizer only

    Divides total amount equally among all current contributors
    and updates their contribution amounts.

    Example: 3000 MKD / 3 contributors = 1000 MKD each
    """
    service = BirthdayService(db)
    birthday = service.calculate_contribution_amounts(birthday_id, current_user_id)
    return birthday


@router.post("/generate", status_code=status.HTTP_201_CREATED)
def generate_birthday_entries(
        db: Session = Depends(get_db)
):
    """
    Auto-generate birthday entries for next 2 months.
    System/Cron job endpoint

    Creates birthday entries for all users with birthdays
    in the next 2 months. Should be called:
    - Monthly by cron job
    - Or manually when needed

    Note: Only creates entries that don't exist yet.
    """
    service = BirthdayService(db)
    birthdays = service.create_birthday_entries()
    return {
        "created_count": len(birthdays),
        "birthdays": [BirthdayResponseSchema.model_validate(b) for b in birthdays]
    }


@router.get("/organized/me", response_model=List[BirthdayWithContributionsSchema])
def get_my_organized_birthdays(
        current_user_id: UUID = Depends(get_current_user_id),
        db: Session = Depends(get_db)
):
    """
    Get all birthdays organized by current user.
    Shows full details including all contributions and payment status.
    """
    service = BirthdayService(db)
    birthdays = service.get_birthdays_organized_by_user(current_user_id)
    return birthdays