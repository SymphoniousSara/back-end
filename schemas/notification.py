import uuid
from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, EmailStr

class NotificationBase(BaseModel):
    type: str
    scheduled_at: Optional[datetime] = None

class NotificationCreate(NotificationBase):
    pass

class NotificationResponse(NotificationBase):
    id: uuid.UUID
    user_id: uuid.UUID
    birthday_id: uuid.UUID
    sent_at: Optional[datetime] = None
    is_sent: bool
    created_at: datetime

    class Config:
        orm_mode = True