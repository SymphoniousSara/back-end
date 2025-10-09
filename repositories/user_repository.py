from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import date

from models.users import User
from repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def email_exists(self, email: str) -> bool:
        return self.db.query(User).filter(User.email == email).first() is not None

    def get_users_with_birthdays_in_range(self, start_date: date, end_date: date) -> List[User]:
        return self.db.query(User).filter(
            User.birth_date.isnot(None),
            User.birth_date >= start_date,
            User.birth_date <= end_date
        ).all()

    #Restriction for personal birthday
    def get_all_except(self, user_id: UUID) -> List[User]:
        # ⚠️ FIXED: Return type should be List[User], not list[type[User]]
        return self.db.query(User).filter(
            User.id != user_id
        ).all()
