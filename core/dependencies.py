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


async def get_current_user_id(
        x_user_id: Optional[str] = Header(None),
        db: Session = Depends(get_db)
) -> UUID:
    """
    Mock authentication dependency.

    Until OAuth is implemented, this accepts a user ID via header.
    In production, this will validate OAuth tokens and extract user info.

    Usage in testing/development:
        Send header: X-User-Id: <uuid>

    Args:
        x_user_id: User ID from header
        db: Database session

    Returns:
        User UUID

    Raises:
        HTTPException: If authentication fails
    """
    if not settings.MOCK_AUTH_ENABLED:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="OAuth authentication not yet implemented"
        )

    if not x_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-User-Id header (mock auth mode)",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id = UUID(x_user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

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