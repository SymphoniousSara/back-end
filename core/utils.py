import re
from typing import Tuple
from fastapi import HTTPException, status
from core.config import settings


def parse_name_from_email(email: str) -> Tuple[str, str]:
    # Validate company domain first
    if not validate_company_email(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email must be from {settings.COMPANY_EMAIL_DOMAIN} domain"
        )

    # Extract local part before @
    match = re.match(r'^([^@]+)@', email)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    local_part = match.group(1)

    # Split by dots
    parts = local_part.split('.')

    if len(parts) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email must be in format: first.last@company.com"
        )

    first_name = parts[0].capitalize()
    last_name = parts[-1].capitalize()

    return first_name, last_name


def validate_company_email(email: str) -> bool:
    domain = settings.COMPANY_EMAIL_DOMAIN
    pattern = rf'^[a-z0-9._%+-]+@{re.escape(domain)}$'
    return bool(re.match(pattern, email.lower()))