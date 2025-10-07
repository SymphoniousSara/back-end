from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session

from models.users import User
from repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super(BaseRepository, self).__init__(User,db)

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def email_exists(self, email: str) -> bool:
        return self.db.query(User).filter(User.email == email).count() != 0

    def get_users_with_birthdays_in_range(self, start_date, end_date) -> list[type[User]]:
        return self.db.query(User).filter(
            User.birthday.isnot(None),
            User.birthday >= start_date,
            User.birthday <= end_date
        ).all()

    #Restriction for personal birthday
    def get_all_except(self, user_id: UUID) -> list[type[User]]:
        return self.db.query(User).filter(
            User.id != user_id
        ).all()
