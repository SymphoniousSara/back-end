from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime, date
from uuid import UUID

class UserBaseSchema(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    nickname: Optional[str] = Field(None, max_length=50)
    birth_date: Optional[date] = None  # Changed from 'birthday' and datetime→date
    role: str = Field(default="user")
    bank_details: Optional[dict] = None

    model_config = {"from_attributes": True}

    @field_validator('birth_date')
    @classmethod
    def validate_birth_date(cls, value):
        if value:
            today = date.today()
            age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
            if age < 18:
                raise ValueError("User must be at least 18 years old")
        return value

class UserCreateSchema(BaseModel):
    email: EmailStr
    model_config = {"from_attributes": True}

class UserUpdateSchema(BaseModel):
    nickname: Optional[str] = Field(None, max_length=50)
    birth_date: Optional[datetime] = None
    bank_details: Optional[dict] = None

    model_config = {"from_attributes": True}

    @field_validator('birth_date')
    @classmethod
    def validate_birth_date(cls, value):
        if value:
            today = date.today()
            age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
            if age < 18:
                raise ValueError("User must be at least 18 years old")
        return value

class UserResponseSchema(UserBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

class UserPublicSchema(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    nickname: Optional[str]
    birth_date: Optional[date] = None
    bank_details: Optional[dict] = None

    model_config = {"from_attributes": True}