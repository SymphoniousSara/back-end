from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from uuid import UUID

from db.database import get_db
from core.dependencies import get_current_user_id
from schemas.birthdays import (
    BirthdayResponseSchema,
    BirthdayUpdate,
    BirthdayWithContributionsSchema
)
from services.birthday_service import BirthdayService

router = APIRouter(prefix="/birthdays", tags=["Birthdays"])


@router.get("", response_model=List[BirthdayWithContributionsSchema])
def list_upcoming_birthdays(
        months_ahead: int = Query(2, ge=1, le=6, description="Months to look ahead"),
        current_user_id: UUID = Depends(get_current_user_id),
        db: Session = Depends(get_db)
):
    """
    List upcoming birthdays in the next 2 months.

    Returns birthdays with:
    - User info (birthday person)
    - Organizer info
    - Contributions list
    - Gift details
    """
    service = BirthdayService(db)
    birthdays = service.get_upcoming_birthdays(current_user_id, months_ahead)
    return birthdays


@router.get("/{birthday_id}", response_model=BirthdayWithContributionsSchema)
def get_birthday_details(
        birthday_id: UUID,
        current_user_id: UUID = Depends(get_current_user_id),
        db: Session = Depends(get_db)
):
    """
    Get detailed birthday information.

    **Visibility depends on role:**
    - **Non-contributor:** See basic info, gift idea, organizer
    - **Contributor:** See above + amount they need to pay, payment status
    - **Organizer:** See everything + can edit details
    """
    service = BirthdayService(db)
    birthday = service.get_birthday_details(birthday_id, current_user_id)
    return birthday


@router.put("/{birthday_id}", response_model=BirthdayResponseSchema)
def update_birthday(
        birthday_id: UUID,
        update_data: BirthdayUpdate,
        current_user_id: UUID = Depends(get_current_user_id),
        db: Session = Depends(get_db)
):
    """
    Update birthday details.

    **Only organizer can update:**
    - Assign themselves as organizer
    - Set gift description
    - Set total amount

    """
    service = BirthdayService(db)
    birthday = service.update_birthday(birthday_id, current_user_id, update_data)
    return birthday


@router.post("/{birthday_id}/assign-organizer", response_model=BirthdayResponseSchema)
def assign_organizer(
        birthday_id: UUID,
        update_data: BirthdayUpdate,
        current_user_id: UUID = Depends(get_current_user_id),
        db: Session = Depends(get_db)
):

    # Convenience endpoint for becoming organizer in one action.
    service = BirthdayService(db)
    birthday = service.assign_organizer_and_details(
        birthday_id,
        current_user_id,
        update_data
    )
    return birthday


@router.post("/generate", status_code=status.HTTP_201_CREATED)
def generate_birthday_entries(
        db: Session = Depends(get_db)
):
    """
    Auto-generate birthday entries for next 2 months.

    **System/Cron job endpoint**

    Creates birthday entries for all users with birthdays
    in the next 2 months. Should be called:
    - Monthly by cron job
    - Or manually when needed

    **Note:** Only creates entries that don't exist yet.
    """
    service = BirthdayService(db)
    birthdays = service.create_birthday_entries()
    return {
        "created_count": len(birthdays),
        "birthdays": birthdays
    }


@router.get("/organized/me", response_model=List[BirthdayWithContributionsSchema])
def get_my_organized_birthdays(
        current_user_id: UUID = Depends(get_current_user_id),
        db: Session = Depends(get_db)
):

    # Useful for organizers to see all their responsibilities.
    service = BirthdayService(db)
    birthdays = service.get_birthdays_organized_by_user(current_user_id)
    return birthdays