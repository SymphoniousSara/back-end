from psycopg2._psycopg import Decimal
from pydantic import BaseModel, Field, field_validator, root_validator
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, date
from uuid import UUID

if TYPE_CHECKING:
    from schemas.contributions import ContributionWithContributorSchema
    from schemas.users import UserPublicSchema

class BirthdayBaseSchema(BaseModel):
    date_year: date
    gift_description: str = Field(..., min_length=1, max_length=5000)

    @field_validator('date_year')
    @classmethod
    def validate_date_year(cls, value):
        if value < date.today():
            raise ValueError('Birthday date cannot be in the past')
        return value

class BirthdayCreateSchema(BirthdayBaseSchema):
    user_id: UUID

    @field_validator()
    def check_user_and_organizer_diff(cls, values):
        if values.get('user_id') == values.get('organizer_id'):
            raise ValueError('Organizer cannot be the same person as the birthday person')
        return values

class BirthdayUpdate(BaseModel):
    date_year: Optional[date] = None
    gift_description: Optional[str] = Field(None, min_length=1, max_length=5000)

    @field_validator('date_year')
    @classmethod
    def validate_date_year(cls, value):
        if value is not None and value < date.today():
            raise ValueError('Birthday date cannot be in the past')
        return value

class BirthdayResponseSchema(BirthdayBaseSchema):
    id: UUID
    user_id: UUID
    organizer_id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }

class BirthdayWithDetailsSchema(BirthdayResponseSchema):
    user: "UserPublicSchema"
    organizer: "UserPublicSchema"

    model_config = {
        "from_attributes": True
    }

class BirthdayWithContributionsSchema(BirthdayWithDetailsSchema):
    contributions: List["ContributionWithContributorSchema"] = []
    total_amount: Optional[Decimal] = None
    total_paid: Optional[Decimal] = None

    model_config = {
        "from_attributes": True
    }