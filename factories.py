# factories.py (updated)
import uuid
from datetime import datetime, date, timedelta
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session

from models.users import User
from models.birthdays import Birthday
from models.gifts import Gift
from models.contributions import Contribution


class UserFactory:
    """Factory for creating test users."""

    @staticmethod
    def create(
            db: Session,
            email: Optional[str] = None,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            nickname: Optional[str] = None,
            birth_date: Optional[date] = None,
            role: str = "user",
            **kwargs
    ) -> User:
        """Create a test user."""
        if not email:
            random_id = str(uuid.uuid4())[:8]
            email = f"test.user{random_id}@symphony.is"

        if not first_name:
            first_name = "Test"

        if not last_name:
            last_name = "User"

        user = User(
            id=uuid.uuid4(),
            email=email,
            first_name=first_name,
            last_name=last_name,
            nickname=nickname,
            birth_date=birth_date,
            role=role,
            **kwargs
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def create_batch(db: Session, count: int = 5) -> List[User]:
        """Create multiple test users."""
        users = []
        for i in range(count):
            user = UserFactory.create(
                db,
                email=f"user{i}@symphony.is",
                first_name=f"User{i}",
                last_name=f"Test{i}",
                birth_date=date(1990 + i, (i % 12) + 1, (i % 28) + 1)
            )
            users.append(user)
        return users


class GiftFactory:
    """Factory for creating test gifts."""

    @staticmethod
    def create(
            db: Session,
            user_id: uuid.UUID,
            name: Optional[str] = None,
            description: Optional[str] = None,
            link: Optional[str] = None,
            **kwargs
    ) -> Gift:
        """Create a test gift."""
        if not name:
            name = f"Test Gift {str(uuid.uuid4())[:8]}"

        if not description:
            description = "A wonderful gift idea"

        gift = Gift(
            id=uuid.uuid4(),
            user_id=user_id,
            name=name,
            description=description,
            link=link,
            **kwargs
        )
        db.add(gift)
        db.commit()
        db.refresh(gift)
        return gift

    @staticmethod
    def create_wishlist(
            db: Session,
            user_id: uuid.UUID,
            count: int = 3
    ) -> list[Gift]:
        """Create multiple gifts for a user's wishlist."""
        gifts = []
        for i in range(count):
            gift = GiftFactory.create(
                db,
                user_id=user_id,
                name=f"Gift Idea {i + 1}",
                description=f"Description for gift {i + 1}",
                link=f"https://example.com/gift{i + 1}"
            )
            gifts.append(gift)
        return gifts

class BirthdayFactory:
    """Factory for creating test birthdays."""

    @staticmethod
    def create(
            db: Session,
            celebrant_id: uuid.UUID,
            organizer_id: Optional[uuid.UUID] = None,
            celebration_date: Optional[date] = None,
            gift_description: Optional[str] = None,
            total_amount: Optional[int] = None,
            **kwargs
    ) -> Birthday:
        """Create a test birthday."""
        if not celebration_date:
            celebration_date = date.today() + timedelta(days=30)

        if not gift_description:
            gift_description = "A special gift for a special person"

        if not total_amount:
            total_amount = 3000

        birthday = Birthday(
            id=uuid.uuid4(),
            celebrant_id=celebrant_id,
            organizer_id=organizer_id,
            celebration_date=celebration_date,
            gift_description=gift_description,
            total_amount=total_amount,
            **kwargs
        )
        db.add(birthday)
        db.commit()
        db.refresh(birthday)
        return birthday


class ContributionFactory:
    """Factory for creating test contributions."""

    @staticmethod
    def create(
            db: Session,
            birthday_id: uuid.UUID,
            contributor_id: uuid.UUID,
            amount: Optional[int] = None,
            paid: bool = False,
            **kwargs
    ) -> Contribution:
        """Create a test contribution."""
        if not amount:
            amount = 300

        contribution = Contribution(
            id=uuid.uuid4(),
            birthday_id=birthday_id,
            contributor_id=contributor_id,
            amount=amount,
            paid=paid,
            **kwargs
        )
        db.add(contribution)
        db.commit()
        db.refresh(contribution)
        return contribution