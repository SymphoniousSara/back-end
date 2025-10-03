import uuid
import uuid
from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, EmailStr

class BirthdayBase(BaseModel):
     date: datetime.datetime
     status: str

class BirthdayCreate(BirthdayBase):
    pass

class BirthdayResponse(BirthdayBase):
    id: uuid.UUID

    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True

