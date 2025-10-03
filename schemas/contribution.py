from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, TYPE_CHECKING, Annotated
from decimal import Decimal

if TYPE_CHECKING:
    from backend.schemas.birthday import BirthdayResponseSchema
    from backend.schemas.users import UserResponseSchema
    from backend.schemas.organizer import OrganizerResponseSchema

class ContributionBaseSchema(BaseModel):
    amount: Annotated[
        Decimal,
        Field(gt=0, max_digits=12, decimal_places=2, description="Contribution amount (must be positive)")
    ]
    paid: bool = False

class ContributionCreateSchema(ContributionBaseSchema):
    birthday_id: UUID
    contributor_id: UUID
    organizer_id: Optional[UUID] = None

class ContributionUpdateSchema(BaseModel):
    amount: Optional[Annotated[Decimal, Field(gt=0, max_digits=12, decimal_places=2)]] = None
    paid: Optional[bool] = None
    organizer_id: Optional[UUID] = None

class ContributionResponseSchema(ContributionBaseSchema):
    id: UUID
    birthday_id: UUID
    contributor_id: UUID
    organizer_id: Optional[UUID] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Extended schema with relationships
class ContributionWithRelationsSchema(ContributionResponseSchema):
    birthday: Optional["BirthdayResponseSchema"] = None
    contributor: Optional["UserResponseSchema"] = None
    organizer: Optional["OrganizerResponseSchema"] = None

    class Config:
        from_attributes = True