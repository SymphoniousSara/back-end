from sqlalchemy import Column, String, DateTime, ForeignKey, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from backend.db.database import Base
import uuid

class Birthday(Base):
    __tablename__ = "birthdays"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String, default="planned")  # planned | collecting | gift_decided | completed | cancelled
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="birthdays")
    organizer = relationship("Organizer", back_populates="birthday", uselist=False, cascade="all, delete-orphan")
    contributions = relationship("Contribution", back_populates="birthday", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="birthday", cascade="all, delete-orphan")