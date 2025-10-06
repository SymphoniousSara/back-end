from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserBaseSchema(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    nickname: Optional[str] = Field(None, max_length=50)
    birthday: Optional[datetime] = None
    role: str = Field(default="user")
    bank_details: Optional[dict] = None

    @field_validator('birthday')
    @classmethod
    def validate_birthday(cls, value):
        if value and value > datetime.now():
            raise ValueError('Birthday cannot be in the future')
        return value

class UserCreateSchema(UserBaseSchema):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    nickname: Optional[str] = Field(None, max_length=50)
    birthday: Optional[datetime] = None
    bank_details: Optional[dict] = None


class UserUpdateSchema(UserBaseSchema):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    nickname: Optional[str] = Field(None, max_length=50)
    birthday: Optional[datetime] = None
    bank_details: Optional[dict] = None

    @field_validator('birthday')
    @classmethod
    def validate_birthday(cls, value):
        if value and value > datetime.now():
            raise ValueError('Birthday cannot be in the future')
        return value

class UserResponseSchema(UserBaseSchema):
    id: UUID
    email: str
    first_name: str
    last_name: str
    nickname: Optional[str]
    birthday: Optional[datetime]
    role: str
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }

class UserPublicSchema(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    nickname: Optional[str]

    model_config = {
        "from_attributes": True
    }