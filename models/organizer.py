from sqlalchemy import Column, DateTime, ForeignKey, Numeric, UniqueConstraint, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from db.database import Base
import uuid

class Organizer(Base):
    __tablename__ = "organizers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    birthday_id = Column(UUID(as_uuid=True), ForeignKey("birthdays.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    gift_description = Column(Text, nullable=True)
    total_amount = Column(Numeric(12, 2), default=3000)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    __table_args__ = (UniqueConstraint("birthday_id", "user_id", name="uq_birthday_organizer"),)

    # Relationships
    birthday = relationship("Birthday", back_populates="organizer")
    organizer = relationship("User", back_populates="organizer_roles")
    contributions = relationship("Contribution", back_populates="organizer")
