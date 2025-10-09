from sqlalchemy import Column, DateTime, ForeignKey, Date, Text, UniqueConstraint, CheckConstraint, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from db.database import Base
import uuid

class Birthday(Base):
    __tablename__ = "birthdays"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    celebrant_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    organizer_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False) #organizer
    celebration_date = Column(Date, nullable=False) #yearly iteration of each birthday
    gift_description = Column(Text, nullable=True) #organizer's proposal - for now
    total_amount = Column(Integer, nullable=True) # 3000mkd recommended
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    __table_args__ = (
        CheckConstraint("celebrant_id <> organizer_id", name="ck_celebrant_not_organizer"),
        UniqueConstraint("celebrant_id", "celebration_date", name="uq_celebrant_birthday_date")
    )

    # Relationships
    celebrant = relationship("User", back_populates="birthdays_as_celebrant", foreign_keys=[celebrant_id])
    organizer = relationship("User", back_populates="birthdays_as_organizer", foreign_keys=[organizer_id])
    contributions = relationship("Contribution", back_populates="birthday")