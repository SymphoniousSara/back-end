from typing import Generic, Optional, TypeVar, Type, List
from uuid import UUID
from sqlalchemy.orm import Session
from db.database import Base

from models.contributions import Contribution
from repositories.base import BaseRepository

class UserRepository(BaseRepository[Contribution]):
    def __init__(self, db: Session):
        super(BaseRepository, self).__init__(Contribution,db)