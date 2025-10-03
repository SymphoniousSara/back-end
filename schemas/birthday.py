from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime
from typing import Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from backend.schemas.users import UserResponseSchema
    from backend.schemas.organizer import OrganizerResponseSchema
    from backend.schemas.contribution import ContributionResponseSchema
    from backend.schemas.notification import NotificationResponseSchema

class BirthdayBaseSchema(BaseModel):
    date: date
    status: Literal["planned", "collecting", "gift_decided", "completed", "cancelled"] = "planned"

class BirthdayCreateSchema(BirthdayBaseSchema):
    user_id: UUID

class BirthdayUpdateSchema(BaseModel):
    date: Optional[date] = None
    status: Optional[Literal["planned", "collecting", "gift_decided", "completed", "cancelled"]] = None

class BirthdayResponseSchema(BirthdayBaseSchema):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Enables ORM mode for SQLAlchemy compatibility

# Extended schema with relationships
class BirthdayWithRelations(BirthdayResponseSchema):
    """Extended schema with relationships - use specific models instead of dict"""
    user: Optional["UserResponseSchema"] = None
    organizer: Optional["OrganizerResponseSchema"] = None
    contributions: list["ContributionResponseSchema"] = []
    notifications: list["NotificationResponseSchema"] = []

    class Config:
        from_attributes = True