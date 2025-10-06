from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from backend.db.database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    nickname = Column(String, nullable=True)
    birthday = Column(DateTime, nullable=True)
    role = Column(String, default="user") # Future improvement: admin
    bank_details = Column(JSONB, nullable=True)  # encrypted at rest
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    wishlists = relationship("Wishlist", back_populates="user", cascade="all, delete-orphan")
    birthdays = relationship("Birthday", back_populates="user", cascade="all, delete-orphan")
    contributions = relationship("Contribution", back_populates="contributor", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    organizer_roles = relationship("Organizer", back_populates="organizer", cascade="all, delete-orphan")