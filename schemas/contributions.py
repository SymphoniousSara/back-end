from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from uuid import UUID
from sqlalchemy import Numeric

from schemas.users import UserPublicSchema

if TYPE_CHECKING:
    from schemas.birthdays import BirthdayResponseSchema
    from schemas.users import UserResponseSchema

class ContributionBaseSchema(BaseModel):
    amount: Optional[Numeric] = Field(..., gt=0, max_digits=12, decimal_places=2)
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, value):
        if value <= 0:
            raise ValueError('Amount must be greater than 0')
        return value


class ContributionCreateSchema(ContributionBaseSchema):
    birthday_id: UUID

class ContributionUpdateSchema(BaseModel):
    amount: Optional[Numeric] = Field(None, gt=0, max_digits=12, decimal_places=2)
    paid: Optional[bool] = None

    model_config = {"from_attributes": True}

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, value):
        if value is not None and value <= 0:
            raise ValueError('Amount must be greater than 0')
        return value

class ContributionResponseSchema(ContributionBaseSchema):
    id: UUID
    birthday_id: UUID
    contributor_id: UUID
    paid: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class ContributionSummary(BaseModel):
    total_contributions: int
    total_amount: Numeric
    total_paid: Numeric
    total_unpaid: Numeric

    model_config = ConfigDict(arbitrary_types_allowed=True)

class ContributionWithRelationsSchema(ContributionResponseSchema):
    birthday: Optional["BirthdayResponseSchema"] = None
    contributor: Optional["UserResponseSchema"] = None

    model_config = {
        "from_attributes": True
    }

class ContributionWithContributorSchema(ContributionResponseSchema):
    contributor: "UserPublicSchema"

    model_config = {
        "from_attributes": True
    }