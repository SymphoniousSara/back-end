from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from backend.schemas.users import UserResponseSchema
    from backend.schemas.birthday import BirthdayResponseSchema

class NotificationBaseSchema(BaseModel):
    type: Literal["monthly_reminder", "gift_invite", "payment_request", "birthday_wish"] = Field(
        ...,
        description="Type of notification"
    )
    birthday_id: Optional[UUID] = None
    scheduled_at: Optional[datetime] = None

class NotificationCreateSchema(NotificationBaseSchema):
    user_id: UUID

class NotificationUpdateSchema(BaseModel):
    type: Optional[Literal["monthly_reminder", "gift_invite", "payment_request", "birthday_wish"]] = None
    birthday_id: Optional[UUID] = None
    scheduled_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    is_sent: Optional[bool] = None

class NotificationResponseSchema(NotificationBaseSchema):
    id: UUID
    user_id: UUID
    sent_at: Optional[datetime] = None
    is_sent: bool = False
    created_at: datetime

    class Config:
        from_attributes = True

class NotificationWithRelationsSchema(NotificationResponseSchema):
    """Extended schema with relationships"""
    user: Optional["UserResponseSchema"] = None
    birthday: Optional["BirthdayResponseSchema"] = None

    class Config:
        from_attributes = True