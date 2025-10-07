from typing import Generic, Optional, TypeVar, Type, List, Any
from uuid import UUID
from sqlalchemy.orm import Session
from db.database import Base

from models.gifts import Gift
from repositories.base import BaseRepository

class GiftRepository(BaseRepository[Gift]):
    def __init__(self, db: Session):
        super(BaseRepository, self).__init__(Gift,db)

    def get_by_user_id(self, user_id: UUID) -> list[type[Gift]]:
        return self.db.query(Gift).filter(Gift.user_id == user_id).all()

    def count_user_gifts(self, user_id: UUID) -> int:
        return self.db.query(Gift).filter(Gift.user_id == user_id).count()
