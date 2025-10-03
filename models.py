from sqlalchemy import (Column, String,Date,
    DateTime,Text,Numeric,Boolean,ForeignKey,UniqueConstraint,func)
from sqlalchemy.orm import relationship
from database import Base
import uuid

class Wishlist(Base):
    __tablename__ = "wishlists"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    link = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="wishlists")


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


class Contribution(Base):
    __tablename__ = "contributions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    birthday_id = Column(UUID(as_uuid=True), ForeignKey("birthdays.id", ondelete="CASCADE"), nullable=False)
    contributor_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    organizer_id = Column(UUID(as_uuid=True), ForeignKey("organizers.id", ondelete="SET NULL"), nullable=True)
    amount = Column(Numeric(12, 2), nullable=False)
    paid = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (UniqueConstraint("birthday_id", "contributor_id", name="uq_contribution_unique"),)

    # Relationships
    birthday = relationship("Birthday", back_populates="contributions")
    contributor = relationship("User", back_populates="contributions")
    organizer = relationship("Organizer", back_populates="contributions")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type = Column(String, nullable=False)  # monthly_reminder | gift_invite | payment_request | birthday_wish
    birthday_id = Column(UUID(as_uuid=True), ForeignKey("birthdays.id", ondelete="SET NULL"), nullable=True)
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    is_sent = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="notifications")
    birthday = relationship("Birthday", back_populates="notifications")

