# Vibe coded until actual OAuth is implemented. ;) Working with mock data for testing.
from typing import Generator, Optional
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from uuid import UUID

from db.database import SessionLocal
from models.users import User
from core.config import settings


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user_id():
    user_id = UUID("e6124687-61f1-4c74-a858-2244379c898f")
    return user_id


async def get_current_user(
        user_id: UUID = Depends(get_current_user_id),
        db: Session = Depends(get_db)
) -> User:
    """
    Get the current authenticated user object.

    Args:
        user_id: Current user's ID
        db: Database session

    Returns:
        User object

    Raises:
        HTTPException: If user not found
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


# TODO: Replace with OAuth implementation
# Example OAuth dependency (to be implemented):
"""
from fastapi.security import OAuth2AuthorizationCodeBearer

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/auth",
    tokenUrl="https://oauth2.googleapis.com/token",
)

async def get_current_user_oauth(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    # Validate OAuth token
    # Extract user email from token
    # Get or create user from database
    # Return user object
    pass
"""