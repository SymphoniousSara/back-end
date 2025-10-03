import numbers
import uuid
from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel

class OrganizerBase(BaseModel):
    gift_description: Optional[str]
    total_amount: Optional[numbers.Number]

class UserResponse(OrganizerBase):
    id: uuid.UUID
    birthday_id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True