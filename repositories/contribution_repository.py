from typing import Generic, Optional, TypeVar, Type, List, Any
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from db.database import Base

from models.contributions import Contribution
from repositories.base import BaseRepository

class UserRepository(BaseRepository[Contribution]):
    def __init__(self, db: Session):
        super(BaseRepository, self).__init__(Contribution,db)

    def get_by_birthday_id(self, birthday_id: UUID) -> list[type[Contribution]]:
        # Getting all the contributors by birthday_id
        return self.db.query(Contribution).filter(
            Contribution.birthday_id == birthday_id
        ).options(
            joinedload(Contribution.contributions)
        ).all()
    def get_by_contributor_id(self, contributor_id: UUID) -> list[type[Contribution]]:
        return self.db.query(Contribution).filter(
            Contribution.contributor_id == contributor_id
        ).options(
            joinedload(Contribution.birthday).joinedload('user_id')
        ).all()