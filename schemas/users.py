from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserBaseSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    nickname: Optional[str] = Field(None, max_length=50)
    birthday: Optional[datetime] = None
    role: str = Field(default="user")
    bank_details: Optional[dict] = None

    model_config = {"from_attributes": True}

    @field_validator('birthday')
    @classmethod
    def validate_birthday(cls, value):
        if value:
            today = datetime.now().date()
            age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
            if age < 18:
                raise ValueError("User must be at least 18 years old to be employed.")
        return value

class UserCreateSchema(UserBaseSchema):
    # the user will be automatically created on first login - first and last name extracted from email
    birthday: Optional[datetime] = None
    # email: EmailStr
    # first_name: str = Field(..., min_length=1, max_length=100)
    # last_name: str = Field(..., min_length=1, max_length=100)
    # nickname: Optional[str] = Field(None, max_length=50)
    # bank_details: Optional[dict] = None


class UserUpdateSchema(UserBaseSchema):
    nickname: Optional[str] = Field(None, max_length=50)
    birthday: Optional[datetime] = None
    bank_details: Optional[dict] = None

    model_config = {"from_attributes": True}

    @field_validator('birthday')
    @classmethod
    def validate_birthday(cls, value):
        if value:
            today = datetime.now().date()
            age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
            if age < 18:
                raise ValueError("User must be at least 18 years old to be employed.")
        return value

# Maybe will be decluttered later, not sure if all fields are needed.
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