from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.gifts import Gift
from repositories.gift_repository import GiftRepository
from schemas.gifts import GiftCreateSchema, GiftUpdateSchema


class GiftService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = GiftRepository(db)

    def add_gift_to_wishlist(
            self,
            user_id: UUID,
            gift_data: GiftCreateSchema
    ) -> Gift:

        gift = self.repository.create(
            user_id=user_id,
            name=gift_data.name,
            description=gift_data.description,
            link=gift_data.link
        )
        return gift

    def get_user_wishlist(self, user_id: UUID) -> list[type[Gift]]:
        return self.repository.get_by_user_id(user_id)

    def get_gift_by_id(
            self,
            gift_id: UUID,
            current_user_id: UUID
    ) -> Gift:
        gift = self.repository.get_by_id(gift_id)
        if not gift:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Gift not found"
            )

    def update_gift(
            self,
            gift_id: UUID,
            current_user_id: UUID,
            update_data: GiftUpdateSchema
    ) -> Gift:

        # Verify ownership
        gift = self.get_gift_by_id(gift_id, current_user_id)

        # Update only provided fields
        update_dict = update_data.model_dump(exclude_unset=True)

        updated_gift = self.repository.update(gift_id, **update_dict)
        if not updated_gift:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Gift not found"
            )

        return updated_gift

    def delete_gift(
            self,
            gift_id: UUID,
            current_user_id: UUID
    ) -> bool:

        # Verify ownership
        gift = self.get_gift_by_id(gift_id, current_user_id)

        success = self.repository.delete(gift_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Gift not found"
            )

        return success

    def get_public_wishlist(self, user_id: UUID) -> list[type[Gift]]:
        return self.repository.get_by_user_id(user_id)