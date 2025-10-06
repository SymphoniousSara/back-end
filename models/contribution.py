from sqlalchemy import Column, DateTime, ForeignKey, Numeric, Boolean, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from db.database import Base
import uuid

class Contribution(Base):
    __tablename__ = "contributions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    birthday_id = Column(UUID(as_uuid=True), ForeignKey("birthdays.id", ondelete="CASCADE"), nullable=False)
    contributor_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    paid = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (UniqueConstraint("birthday_id", "contributor_id", name="uq_contribution_unique"),)

    # Relationships
    birthday = relationship("Birthday", back_populates="contributions")
    contributor = relationship("User", back_populates="contributions")