import datetime, uuid
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List, Annotated, Optional
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# ----------------------
# SCHEMAS
# ----------------------

# Base schema (shared fields, but no id/timestamps)
class UserBase(BaseModel):
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = "user"
    bank_details: Optional[dict] = None


# Request schema (what client sends when creating a user)
class UserCreate(UserBase):
    pass


# Response schema (what API returns, includes id + timestamps)
class UserResponse(UserBase):
    id: uuid.UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True  # allows SQLAlchemy model → Pydantic


# ----------------------
# DB DEPENDENCY
# ----------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


# ----------------------
# ROUTES
# ----------------------
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/", response_model=List[UserResponse])
def get_users(db: db_dependency):
    return db.query(models.User).all()
