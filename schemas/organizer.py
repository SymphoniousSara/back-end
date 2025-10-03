from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, TYPE_CHECKING, Annotated
from decimal import Decimal

if TYPE_CHECKING:
    from backend.schemas.birthday import BirthdayResponseSchema
    from backend.schemas.users import UserResponseSchema
    from backend.schemas.contribution import ContributionResponseSchema

class OrganizerBaseSchema(BaseModel):
    gift_description: Optional[str] = None
    total_amount: Annotated[
        Decimal,
        Field(ge=0, max_digits=12, decimal_places=2, description="Total amount for the gift")
    ] = Decimal("3000.00")

class OrganizerCreateSchema(OrganizerBaseSchema):
    birthday_id: UUID
    user_id: UUID

class OrganizerUpdateSchema(BaseModel):
    gift_description: Optional[str] = None
    total_amount: Optional[Annotated[Decimal, Field(ge=0, max_digits=12, decimal_places=2)]] = None

class OrganizerResponseSchema(OrganizerBaseSchema):
    id: UUID
    birthday_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Extended schema with relationships
class OrganizerWithRelationsSchema(OrganizerResponseSchema):
    birthday: Optional["BirthdayResponseSchema"] = None
    organizer: Optional["UserResponseSchema"] = None
    contributions: list["ContributionResponseSchema"] = []

    class Config:
        from_attributes = True