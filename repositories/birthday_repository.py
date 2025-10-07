from typing import Generic, Optional, TypeVar, Type, List
from uuid import UUID
from sqlalchemy.orm import Session
from db.database import Base

from models.birthdays import Birthday
from repositories.base import BaseRepository

class UserRepository(BaseRepository[Birthday]):
    def __init__(self, db: Session):
        super(BaseRepository, self).__init__(Birthday,db)