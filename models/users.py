from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from db.database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    nickname = Column(String, nullable=True)
    birthday = Column(DateTime, nullable=True)
    role = Column(String, default="user") # keeping an option for admin role
    bank_details = Column(JSONB, nullable=True)  # should be encrypted by app or DB extension
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())


    # Relationships
    gifts = relationship("Gift", back_populates="users", cascade="all, delete-orphan")
    birthdays = relationship("Birthday", back_populates="users", cascade="all, delete-orphan", foreign_keys="Birthday.user_id")
    organized_birthdays = relationship("Birthday", back_populates="organizer", cascade="all, delete-orphan", foreign_keys="Birthday.organizer_id")
    contributions = relationship("Contribution", back_populates="contributions", cascade="all, delete-orphan")