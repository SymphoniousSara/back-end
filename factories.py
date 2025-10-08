import uuid
from datetime import datetime, date, timedelta
from decimal import Decimal
from typing import Optional, Dict, Any
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
            birthday: Optional[datetime] = None,
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
            birthday=birthday,
            role=role,
            **kwargs
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def create_batch(db: Session, count: int = 5) -> list[User]:
        """Create multiple test users."""
        users = []
        for i in range(count):
            user = UserFactory.create(
                db,
                email=f"user{i}@symphony.is",
                first_name=f"User{i}",
                last_name=f"Test{i}",
                birthday=datetime(1990 + i, (i % 12) + 1, (i % 28) + 1)
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
            user_id: uuid.UUID,
            organizer_id: uuid.UUID,
            date_year: Optional[date] = None,
            gift_description: Optional[str] = None,
            total_amount: Optional[Decimal] = None,
            **kwargs
    ) -> Birthday:
        """Create a test birthday."""
        if not date_year:
            date_year = date.today() + timedelta(days=30)

        if not gift_description:
            gift_description = "A special gift for a special person"

        if not total_amount:
            total_amount = Decimal('3000.00')

        birthday = Birthday(
            id=uuid.uuid4(),
            user_id=user_id,
            organizer_id=organizer_id,
            date_year=date_year,
            gift_description=gift_description,
            total_amount=total_amount,
            **kwargs
        )
        db.add(birthday)
        db.commit()
        db.refresh(birthday)
        return birthday

    @staticmethod
    def create_upcoming(
            db: Session,
            users: list[User],
            organizer: User
    ) -> list[Birthday]:
        """Create upcoming birthdays for a list of users."""
        birthdays = []
        today = date.today()

        for i, user in enumerate(users):
            if user.id == organizer.id:
                continue  # Skip organizer's own birthday

            birthday_date = today + timedelta(days=(i + 1) * 15)
            birthday = BirthdayFactory.create(
                db,
                user_id=user.id,
                organizer_id=organizer.id,
                date_year=birthday_date,
                gift_description=f"Birthday celebration for {user.first_name}",
                total_amount=Decimal('3000.00')
            )
            birthdays.append(birthday)

        return birthdays


class ContributionFactory:
    """Factory for creating test contributions."""

    @staticmethod
    def create(
            db: Session,
            birthday_id: uuid.UUID,
            contributor_id: uuid.UUID,
            amount: Optional[Decimal] = None,
            paid: bool = False,
            **kwargs
    ) -> Contribution:
        """Create a test contribution."""
        if not amount:
            amount = Decimal('300.00')

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

    @staticmethod
    def create_for_birthday(
            db: Session,
            birthday: Birthday,
            contributors: list[User],
            amount_per_person: Optional[Decimal] = None
    ) -> list[Contribution]:
        """Create contributions for a birthday from multiple users."""
        if not amount_per_person:
            amount_per_person = birthday.total_amount / len(contributors)

        contributions = []
        for contributor in contributors:
            if contributor.id == birthday.user_id:
                continue  # Skip birthday person

            contribution = ContributionFactory.create(
                db,
                birthday_id=birthday.id,
                contributor_id=contributor.id,
                amount=amount_per_person,
                paid=False
            )
            contributions.append(contribution)

        return contributions


class TestDataSeeder:
    """Helper to seed database with complete test scenarios."""

    @staticmethod
    def seed_complete_scenario(db: Session) -> Dict[str, Any]:
        """
        Create a complete test scenario with users, birthdays, gifts, and contributions.

        Returns a dict with all created objects for easy reference in tests.
        """
        # Create users
        users = UserFactory.create_batch(db, count=10)

        # First user is the organizer
        organizer = users[0]

        # Create wishlists for some users
        for user in users[1:4]:
            GiftFactory.create_wishlist(db, user.id, count=3)

        # Create upcoming birthdays
        birthdays = BirthdayFactory.create_upcoming(
            db,
            users=users[1:5],  # 4 birthdays
            organizer=organizer
        )

        # Create contributions for first birthday
        if birthdays:
            first_birthday = birthdays[0]
            contributors = [u for u in users if u.id != first_birthday.user_id][:5]
            ContributionFactory.create_for_birthday(
                db,
                birthday=first_birthday,
                contributors=contributors
            )

        return {
            "users": users,
            "organizer": organizer,
            "birthdays": birthdays,
            "contributors": contributors if birthdays else []
        }