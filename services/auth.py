import traceback
from fastapi import HTTPException, Cookie
from datetime import datetime, timedelta
from jose import jwt, ExpiredSignatureError, JWTError
from dotenv import load_dotenv
import os

load_dotenv(override=True)

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.UTC) + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Cookie(None)):
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Not Authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])

        user_id: str = payload.get("user_id")
        user_email: str = payload.get("email")

        if (user_id is None) or (user_email is None):
            raise HTTPException(
                status_code=401,
                detail="Not Authenticated",
            )

        return {"user_id": user_id, "user_email": user_email}

    except ExpiredSignatureError:
        traceback.print_exc()
        raise HTTPException(
            status_code=401,
            detail="Expired token",
        )
    except JWTError:
        traceback.print_exc()
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=401,
            detail='Not Authenticated'
        )

def validate_user_request(token: str = Cookie(None)):
    session_details = get_current_user(token)

    return session_details
