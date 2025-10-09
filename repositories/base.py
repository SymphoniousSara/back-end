from typing import Generic, TypeVar, Type, Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from db.database import Base

ModelType = TypeVar("ModelType", bound=Base)

# All the CRUD operations are implemented and the rest of the repositories inherit them only specific methods are added/override.
class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, id: UUID) -> Optional[ModelType]:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, **kwargs) -> ModelType:
        db_obj = self.model(**kwargs)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, id: UUID, **kwargs) -> Optional[ModelType]:
        db_obj = self.get_by_id(id)
        if not db_obj:
            return None

        update_data = {k: v for k, v in kwargs.items()
                       if v is not None and hasattr(db_obj, k)}

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, id: UUID) -> bool:
        db_obj = self.get_by_id(id)
        if not db_obj:
            return False

        self.db.delete(db_obj)
        self.db.commit()
        return True

    def exists(self, id: UUID) -> bool:
        return self.db.query(self.model).filter(self.model.id == id).first() is not None

    def count(self) -> int:
        return self.db.query(self.model).count()

    def get_by_field(self, field: str, value: Any) -> Optional[ModelType]:
        if not hasattr(self.model, field):
            return None
        return self.db.query(self.model).filter(getattr(self.model, field) == value).first()

    def get_all_by_field(self, field: str, value: Any) -> List[ModelType]:
        # Example: Get All gifts for a user, get all contributions for a birthday
        if not hasattr(self.model, field):
            return []
        return self.db.query(self.model).filter(getattr(self.model, field) == value).all()

    def bulk_create(self, objects: List[Dict[str, Any]]) -> List[ModelType]:
        db_objs = [self.model(**obj_data) for obj_data in objects]
        self.db.add_all(db_objs)
        self.db.commit()
        for obj in db_objs:
            self.db.refresh(obj)
        return db_objs