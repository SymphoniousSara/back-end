from typing import Generic, TypeVar, Type, Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from db.database import Base

ModelType = TypeVar("ModelType", bound=Base)


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

        for field, value in kwargs.items():
            if value is not None and hasattr(db_obj, field):
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
        return self.db.query(
            self.db.query(self.model).filter(self.model.id == id).exists()
        ).scalar()

    def count(self) -> int:
        return self.db.query(self.model).count()