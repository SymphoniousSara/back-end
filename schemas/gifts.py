from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class GiftBaseSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=255)
    link: Optional[str] = Field(None, max_length=255)

    model_config = {"from_attributes": True}
class GiftCreateSchema(GiftBaseSchema):
    # user_id should be set from authenticated user, not from request body
    pass

class GiftUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=255)
    link: Optional[str] = Field(None, max_length=255)

    model_config = {"from_attributes": True}

class GiftResponseSchema(GiftBaseSchema):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

class GiftWithUserSchema(GiftResponseSchema):
    user: "UserPublicSchema"

    model_config = { "from_attributes": True}