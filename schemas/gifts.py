from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from uuid import UUID

if TYPE_CHECKING:
    from schemas.users import UserPublicSchema

class GiftBaseSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=255)
    link: Optional[str] = Field(None, max_length=255)

class GiftCreateSchema(GiftBaseSchema):
    # user_id should be set from authenticated user, not from request body
    pass

class GiftUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=255)
    link: Optional[str] = Field(None, max_length=255)

class GiftResponseSchema(GiftBaseSchema):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }

class GiftWithUserSchema(GiftResponseSchema):
    user: "UserPublicSchema"

    model_config = {
        "from_attributes": True
    }