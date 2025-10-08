from datetime import datetime
from typing import Optional, TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, ConfigDict
from sqlalchemy import Numeric

from schemas.users import UserPublicSchema

if TYPE_CHECKING:
    from schemas.birthdays import BirthdayResponseSchema
    from schemas.users import UserResponseSchema


class ContributionBaseSchema(BaseModel):
    pass

class ContributionCreateSchema(ContributionBaseSchema):
    birthday_id: UUID
    # contributor_id comes from OAuth

class ContributionUpdateSchema(BaseModel):
    paid: Optional[bool] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

class ContributionResponseSchema(ContributionBaseSchema):
    id: UUID
    birthday_id: UUID
    contributor_id: UUID
    amount: Optional[int] = None
    paid: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ContributionWithRelationsSchema(ContributionResponseSchema):
    birthday: Optional["BirthdayResponseSchema"] = None
    contributor: Optional["UserResponseSchema"] = None

    model_config = ConfigDict(from_attributes=True)

class ContributionWithContributorSchema(ContributionResponseSchema):
    contributor: "UserPublicSchema"

    model_config = ConfigDict(from_attributes=True)

