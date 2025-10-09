from decimal import Decimal
from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from models.contributions import Contribution
from repositories.base import BaseRepository

class ContributionRepository(BaseRepository[Contribution]):
    def __init__(self, db: Session):
        super().__init__(Contribution, db)

    def get_by_birthday_id(self, birthday_id: UUID) -> List[Contribution]:
        return self.db.query(Contribution).filter(
            Contribution.birthday_id == birthday_id
        ).options(
            joinedload(Contribution.contributor)
        ).all()

    def get_by_contributor_id(self, contributor_id: UUID) -> List[Contribution]:
        return self.db.query(Contribution).filter(
            Contribution.contributor_id == contributor_id
        ).options(
            joinedload(Contribution.birthday)
        ).all()

    def get_contribution(
            self,
            birthday_id: UUID,
            contributor_id: UUID
    ) -> Optional[Contribution]:
        # Get a specific contribution by birthday and contributor
        return self.db.query(Contribution).filter(
            Contribution.birthday_id == birthday_id,
            Contribution.contributor_id == contributor_id
        ).first()

    def contribution_exists(
            self,
            birthday_id: UUID,
            contributor_id: UUID
    ) -> bool:
        return self.get_contribution(birthday_id, contributor_id) is not None

    def count_contributors(self, birthday_id: UUID) -> int:
        return self.db.query(Contribution).filter(
            Contribution.birthday_id == birthday_id
        ).count()

    def get_contribution_summary(self, birthday_id: UUID) -> Dict[str, Any]:
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

        total = result.total_amount or 0
        paid = result.paid_amount or 0

        return {
            'contributor_count': result.contributor_count or 0,
            'total_amount': total,
            'paid_amount': paid,
            'unpaid_amount': total - paid  # Simple integer subtraction
        }

    def get_unpaid_contributions(self, birthday_id: UUID) -> List[Contribution]:
        return self.db.query(Contribution).filter(
            Contribution.birthday_id == birthday_id,
            Contribution.paid == False
        ).options(
            joinedload(Contribution.contributor)
        ).all()

    def get_contributions_with_details(self, birthday_id: UUID) -> List[Contribution]:
        # Might implement in organizer view later - for an overview of payment/contributions
        return self.db.query(Contribution).filter(
            Contribution.birthday_id == birthday_id
        ).options(
            joinedload(Contribution.contributor),
            joinedload(Contribution.birthday)
        ).all()