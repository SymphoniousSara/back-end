from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID

from db.database import get_db
from core.dependencies import get_current_user_id
from schemas.gifts import GiftCreateSchema, GiftUpdateSchema, GiftResponseSchema
from services.gift_service import GiftService

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])


@router.get("", response_model=List[GiftResponseSchema])
def get_my_wishlist(
        current_user_id: UUID = Depends(get_current_user_id),
        db: Session = Depends(get_db)
):

    service = GiftService(db)
    gifts = service.get_user_wishlist(current_user_id)
    return gifts


@router.post("", response_model=GiftResponseSchema, status_code=status.HTTP_201_CREATED)
def add_gift_to_wishlist(
        gift_data: GiftCreateSchema,
        current_user_id: UUID = Depends(get_current_user_id),
        db: Session = Depends(get_db)
):
    service = GiftService(db)
    gift = service.add_gift_to_wishlist(current_user_id, gift_data)
    return gift


@router.get("/{gift_id}", response_model=GiftResponseSchema)
def get_gift(
        gift_id: UUID,
        current_user_id: UUID = Depends(get_current_user_id),
        db: Session = Depends(get_db)
):

    # User can only access their own gifts, individually. (For CRUD view)
    service = GiftService(db)
    gift = service.get_gift_by_id(gift_id, current_user_id)
    return gift


@router.put("/{gift_id}", response_model=GiftResponseSchema)
def update_gift(
        gift_id: UUID,
        gift_data: GiftUpdateSchema,
        current_user_id: UUID = Depends(get_current_user_id),
        db: Session = Depends(get_db)
):
    service = GiftService(db)
    gift = service.update_gift(gift_id, current_user_id, gift_data)
    return gift


@router.delete("/{gift_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_gift(
        gift_id: UUID,
        current_user_id: UUID = Depends(get_current_user_id),
        db: Session = Depends(get_db)
):
    service = GiftService(db)
    service.delete_gift(gift_id, current_user_id)
    return None


@router.get("/user/{user_id}", response_model=List[GiftResponseSchema])
def get_user_public_wishlist(
        user_id: UUID,
        db: Session = Depends(get_db)
):
    # View another user's wishlist (public).
    service = GiftService(db)
    gifts = service.get_public_wishlist(user_id)
    return gifts