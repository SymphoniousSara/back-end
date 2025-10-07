from typing import Optional
from uuid import UUID
from datetime import date
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session, joinedload

from models.birthdays import Birthday
from repositories.base import BaseRepository

class BirthdayRepository(BaseRepository[Birthday]):
    def __init__(self, db: Session):
        super(BaseRepository, self).__init__(Birthday,db)

    def get_upcoming_birthdays(
            self,
            months_ahead: int=2,
            include_relations: bool = True
    ) -> list[type[Birthday]]:
    # Usually 2 months ahead - but open-ended cn be twitched later.
        today = date.today()
        end_date = today + relativedelta(months=months_ahead)

        query = self.db.query(Birthday).filter(
            Birthday.date_year >= today,
            Birthday.date_year <= end_date
        )

        if include_relations:
            query = query.options(
                joinedload(Birthday.user),
                joinedload(Birthday.organizer),
                joinedload(Birthday.contributions)
            )

        return query.order_by(Birthday.date_year).all()

    def get_by_birthday_and_year(self, user_id: UUID, year: int) -> Optional[Birthday]:
        # Get birthday celebration for a specific user and year.
        return self.db.query(Birthday).filter(
            Birthday.user_id == user_id,
            Birthday.date_year.between(
                date(year, 1, 1),
                date(year, 12, 31)
            )
        ).first()

    def get_organized_by_user(self, organizer_id: UUID) -> list[type[Birthday]]:
        # All birthdays organized by a specific person.
        return self.db.query(Birthday).filter(
            Birthday.organizer_id == organizer_id
        ).options(
            joinedload(Birthday.user),
            joinedload(Birthday.contributions)
        ).all()

    def get_birthdays_for_user(self, user_id: UUID) -> list[type[Birthday]]:
        # All birthdays organized for a specific person.
        return self.db.query(Birthday).filter(
            Birthday.user_id == user_id
        ).options(
            joinedload(Birthday.organizer),
            joinedload(Birthday.contributions)
        ).order_by(Birthday.date_year.desc()).all()

    def get_all_contributions(self, birthday_id: UUID) -> Optional[Birthday]:
        # Eager-load all contributions for a specific birthday.
        return self.db.query(Birthday).filter(
            Birthday.id == birthday_id
        ).options(
            joinedload(Birthday.user),
            joinedload(Birthday.organizer),
            joinedload(Birthday.contributions).joinedload('contributor')
        ).first()
