from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime
from typing import Optional, Literal

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

# Extended schema with relationships (optional, use when needed)
class BirthdayWithRelationsSchema(BirthdayResponseSchema):
    user: Optional[dict] = None
    organizer: Optional[dict] = None
    contributions: Optional[list[dict]] = None
    notifications: Optional[list[dict]] = None

    class Config:
        from_attributes = True