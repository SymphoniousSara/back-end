from decimal import Decimal
from typing import Optional
from uuid import UUID
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

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

    def get_contribution(
            self,
            birthday_id: UUID,
            contributor_id: UUID
    ) -> Optional[Contribution]:

        return self.db.query(Contribution).filter(
            Contribution.birthday_id == birthday_id,
            Contribution.contributor_id == contributor_id
        ).first()

    def contribution_exists(
            self,
            birthday_id: UUID,
            contributor_id: UUID
    ) -> bool:

        return self.db.query(
            self.db.query(Contribution).filter(
                Contribution.birthday_id == birthday_id,
                Contribution.contributor_id == contributor_id
            ).exists()
        ).scalar()

    def count_contributors(self, birthday_id: UUID) -> int:

        return self.db.query(Contribution).filter(
            Contribution.birthday_id == birthday_id
        ).count()

    def get_contribution_summary(self, birthday_id: UUID) -> dict:
        # Returns: Dictionary with total_amount, paid_amount, unpaid_amount, contributor_count

        result = self.db.query(
            func.count(Contribution.id).label('contributor_count'),
            func.coalesce(func.sum(Contribution.amount), 0).label('total_amount'),
            func.coalesce(
                func.sum(func.case((Contribution.paid == True, Contribution.amount), else_=0)),
                0
            ).label('paid_amount')
        ).filter(
            Contribution.birthday_id == birthday_id
        ).first()

        total = Decimal(str(result.total_amount)) if result.total_amount else Decimal('0')
        paid = Decimal(str(result.paid_amount)) if result.paid_amount else Decimal('0')

        return {
            'contributor_count': result.contributor_count or 0,
            'total_amount': total,
            'paid_amount': paid,
            'unpaid_amount': total - paid
        }

    def get_unpaid_contributions(self, birthday_id: UUID) -> list[type[Contribution]]:
        # Returns a list of contributors who did not pay yet.
        return self.db.query(Contribution).filter(
            Contribution.birthday_id == birthday_id,
            Contribution.paid == False
        ).options(
            joinedload(Contribution.contributions)
        ).all()
