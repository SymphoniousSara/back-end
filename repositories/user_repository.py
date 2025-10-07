from typing import Generic, Optional, TypeVar, Type, List
from uuid import UUID
from sqlalchemy.orm import Session
from db.database import Base

from models.users import User
from repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super(BaseRepository, self).__init__(User,db)


