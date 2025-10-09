from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.users import User
from models.contributions import Contribution
from models.birthdays import Birthday
from models.gifts import Gift
from datetime import date, timedelta
import uuid

def seed_data(db: Session):
    """Seeds the database with example data if empty."""
    if db.query(User).first():
        print("Database already seeded. Skipping...")
        return

    print("Seeding database with sample data...")

    # --- USERS ---
    user_celebrant = User(
        id=uuid.uuid4(),
        email="celebrant@example.com",
        first_name="Alice",
        last_name="Johnson",
        nickname="Ali",
        birth_date=date(1999, 5, 20),
        role="user",
        bank_details={"iban": "MK072000123456789", "bank": "NLB Banka"}
    )

    user_organizer = User(
        id=uuid.uuid4(),
        email="organizer@example.com",
        first_name="Bob",
        last_name="Peterson",
        nickname="Bobby",
        birth_date=date(1997, 9, 15),
        role="user",
        bank_details={"iban": "MK072000987654321", "bank": "Halk Bank"}
    )

    db.add_all([user_celebrant, user_organizer])
    db.commit()

    # --- BIRTHDAY ---
    birthday = Birthday(
        id=uuid.uuid4(),
        celebrant_id=user_celebrant.id,
        organizer_id=user_organizer.id,
        celebration_date=date.today() + timedelta(days=30),
        gift_description="Surprise party and a smartwatch",
        total_amount=5000
    )
    db.add(birthday)
    db.commit()

    # --- CONTRIBUTIONS ---
    contribution_1 = Contribution(
        id=uuid.uuid4(),
        birthday_id=birthday.id,
        contributor_id=user_organizer.id,
        amount=2000,
        paid=True,
    )

    db.add(contribution_1)
    db.commit()

    # --- GIFTS ---
    gift_1 = Gift(
        id=uuid.uuid4(),
        user_id=user_celebrant.id,
        name="Apple Watch SE",
        description="Smartwatch with fitness tracking",
        link="https://apple.com/apple-watch-se"
    )

    gift_2 = Gift(
        id=uuid.uuid4(),
        user_id=user_celebrant.id,
        name="Kindle Paperwhite",
        description="E-reader for book lovers",
        link="https://amazon.com/kindle-paperwhite"
    )

    db.add_all([gift_1, gift_2])
    db.commit()

    print("Database seeded successfully with sample data.")

def run_seed():
    """Utility to manually run seeding if needed."""
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()
