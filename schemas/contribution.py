import numbers
import uuid
from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel

class ContributionBase(BaseModel):
    amount: numbers.Number
    paid: bool

class ContributionCreate(ContributionBase):
    pass

class ContributionResponse(ContributionBase):
    id: uuid.UUID
    birthday_id: uuid.UUID
    organizer_id: uuid.UUID
    contributor_id: uuid.UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True
