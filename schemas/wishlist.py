import datetime
import uuid
from typing import Optional
from pydantic import BaseModel


class WishlistBase(BaseModel):
    title: Optional[str]
    description: Optional[str]
    link: Optional[str]

class WishlistCreate(WishlistBase):
    pass

class WishlistResponse(WishlistBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
