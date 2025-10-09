from typing import Optional, List
from uuid import UUID
from datetime import date
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session, joinedload

from models.birthdays import Birthday
from models.contributions import Contribution
from repositories.base import BaseRepository

class BirthdayRepository(BaseRepository[Birthday]):
    def __init__(self, db: Session):
        super().__init__(Birthday, db)

    def get_upcoming_birthdays(
            self,
            months_ahead: int = 2,
            include_relations: bool = True
    ) -> List[Birthday]:
        today = date.today()
        end_date = today + relativedelta(months=months_ahead)

        query = self.db.query(Birthday).filter(
            Birthday.celebration_date >= today,
            Birthday.celebration_date <= end_date
        )

        if include_relations:
            query = query.options(
                joinedload(Birthday.celebrant),
                joinedload(Birthday.organizer),
                joinedload(Birthday.contributions)
            )

        return query.order_by(Birthday.celebration_date).all()

    def get_by_celebrant_and_year(self, celebrant_id: UUID, year: int) -> Optional[Birthday]:
        return self.db.query(Birthday).filter(
            Birthday.celebrant_id == celebrant_id,
            Birthday.celebration_date.between(
                date(year, 1, 1),
                date(year, 12, 31)
            )
        ).first()

    def get_organized_by_user(self, organizer_id: UUID) -> List[Birthday]:
        return self.db.query(Birthday).filter(
            Birthday.organizer_id == organizer_id
        ).options(
            joinedload(Birthday.celebrant),
            joinedload(Birthday.contributions)
        ).all()

    def get_birthdays_for_celebrant(self, celebrant_id: UUID) -> List[Birthday]:
        return self.db.query(Birthday).filter(
            Birthday.celebrant_id == celebrant_id
        ).options(
            joinedload(Birthday.organizer),
            joinedload(Birthday.contributions)
        ).order_by(Birthday.celebration_date.desc()).all()

    def get_with_contributions(self, birthday_id: UUID) -> Optional[Birthday]:
        # Eager-load all contributions for a specific birthday
        return self.db.query(Birthday).filter(
            Birthday.id == birthday_id
        ).options(
            joinedload(Birthday.celebrant),
            joinedload(Birthday.organizer),
            joinedload(Birthday.contributions).joinedload(Contribution.contributor)
        ).first()

    def get_birthdays_without_organizer(self) -> List[Birthday]:
        return self.db.query(Birthday).filter(
            Birthday.organizer_id.is_(None)
        ).options(
            joinedload(Birthday.celebrant)
        ).all()

    def get_birthdays_by_celebration_date(self, celebration_date: date) -> List[Birthday]:
        return self.db.query(Birthday).filter(
            Birthday.celebration_date == celebration_date
        ).options(
            joinedload(Birthday.celebrant),
            joinedload(Birthday.organizer)
        ).all()