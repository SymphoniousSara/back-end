from datetime import datetime, date
from typing import Optional, List, TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, ConfigDict
from sqlalchemy import Numeric

if TYPE_CHECKING:
    from schemas.contributions import ContributionWithContributorSchema
    from schemas.users import UserPublicSchema
    from schemas.gifts import GiftResponseSchema


class BirthdayBaseSchema(BaseModel):
    celebration_date: date
    gift_description: Optional[str] = Field(..., min_length=1, max_length=5000)
    total_amount: Optional[int] = None

    model_config = {"from_attributes": True}

    @field_validator("celebration_date")
    @classmethod
    def validate_celebration_date(cls, value):
        if value < date.today():
            raise ValueError("Birthday date cannot be in the past")
        return value

class BirthdayCreateSchema(BirthdayBaseSchema):
    celebrant_id: UUID
    # initially no organizer_id needed

class BirthdayUpdateSchema(BaseModel):
    celebration_date: Optional[date] = None
    gift_description: Optional[str] = Field(None, min_length=1, max_length=5000)
    total_amount: Optional[int] = None
    organizer_id: Optional[UUID] = None

    model_config = {"from_attributes": True}

    @field_validator("celebration_date")
    @classmethod
    def validate_celebration_date(cls, value):
        if value is not None and value < date.today():
            raise ValueError("Birthday date cannot be in the past")
        return value

class BirthdayResponseSchema(BirthdayBaseSchema):
    id: UUID
    celebrant_id: UUID
    organizer_id: Optional[UUID] = None
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class BirthdayWithDetailsSchema(BirthdayResponseSchema):
    celebrant: "UserPublicSchema"  # Celebrant info
    organizer: Optional["UserPublicSchema"] = None # Organizer info
    celebrant_gifts: List["GiftResponseSchema"] = []  # Celebrant's wishlist


class BirthdayWithContributionsSchema(BirthdayWithDetailsSchema):
    contributions: List["ContributionWithContributorSchema"] = []
    total_amount: Optional[Numeric] = None

    model_config = ConfigDict(from_attributes=True)
