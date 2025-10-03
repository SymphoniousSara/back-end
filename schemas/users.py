import uuid
from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = "user"
    bank_details: Optional[dict] = None

class UserCreate(UserBase):
    pass # apparently empty cuz reuses everything from UserBase.

class UserResponse(UserBase):
    id: uuid.UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True
