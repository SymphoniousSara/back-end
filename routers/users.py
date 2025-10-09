from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from db.database import get_db
from core.dependencies import get_current_user, get_current_user_id
from schemas.users import UserResponseSchema, UserUpdateSchema, UserPublicSchema
from services.user_service import UserService
from models.users import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/my-profile", response_model=UserResponseSchema)
def get_current_user_profile(
        current_user: User = Depends(get_current_user)
):
    return UserResponseSchema.model_validate(current_user)


@router.put("/my-profile", response_model=UserResponseSchema)
def update_current_user_profile(
        update_data: UserUpdateSchema,
        current_user_id: UUID = Depends(get_current_user_id),
        db: Session = Depends(get_db)
):
    #Editable fields: nickname, birthday, bank_details; static: email, firstname, lastname
    service = UserService(db)
    updated_user = service.update_profile(current_user_id, update_data)
    return UserResponseSchema.model_validate(updated_user)


@router.get("", response_model=List[UserPublicSchema])
def list_users(
        db: Session = Depends(get_db)
):
    service = UserService(db)
    users = service.get_all_users()
    return [UserPublicSchema.model_validate(u) for u in users]
