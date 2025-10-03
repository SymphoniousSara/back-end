from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from backend.schemas.users import UserResponseSchema

class WishlistBaseSchema(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    link: Optional[str] = Field(None, max_length=2048)

class WishlistCreateSchema(WishlistBaseSchema):
    user_id: UUID

class WishlistUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    link: Optional[str] = Field(None, max_length=2048)

class WishlistResponseSchema(WishlistBaseSchema):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Extended schema with relationships"""
class WishlistWithRelationsSchema(WishlistResponseSchema):
    user: Optional["UserResponseSchema"] = None

    class Config:
        from_attributes = True