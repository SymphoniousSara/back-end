from typing import Optional, Any, Dict
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class UserBaseSchema(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = Field(default="user")
    bank_details: Optional[Dict[str, Any]] = None  # JSONB field as dict

class UserCreateSchema(UserBaseSchema):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bank_details: Optional[Dict[str, Any]] = None

class UserUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bank_details: Optional[Dict[str, Any]] = None
    role: Optional[str] = None

class UserResponseSchema(UserBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attribute = True
        orm_mode = True