from sqlalchemy import Column, String, DateTime, ForeignKey, Date, Text, Numeric, UniqueConstraint, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from db.database import Base
import uuid

class Birthday(Base):
    __tablename__ = "birthdays"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False) #birthday_person
    organizer_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False) #organizer
    date_year = Column(Date, nullable=False) #yearly iteration of each birthday
    gift_description = Column(Text, nullable=False) #organizer's proposal - for now
    total_amount=Column(Numeric(asdecimal=2), nullable=False) # 3000mkd recommended
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("birthday_id", "contributor_id", name="uq_contribution_unique"),
        CheckConstraint("user_id <> organizer_id", name="ck_user_not_organizer"),
        UniqueConstraint("user_id", "date_year", name="uq_user_birthday_year")
    )

    # Relationships
    users = relationship("User", back_populates="birthdays", foreign_keys=[user_id])
    organizer = relationship("User", back_populates="organized_birthdays", foreign_keys=[organizer_id])
    contributions = relationship("Contribution", back_populates="birthdays", cascade="all, delete-orphan")