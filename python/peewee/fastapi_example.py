"""Peewee + FastAPI 연동 패턴 예제."""

from contextlib import asynccontextmanager
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from playhouse.shortcuts import model_to_dict
from pydantic import BaseModel as PydanticBase

from database import db
from models import ALL_TABLES, User


# ── Pydantic 스키마 ──────────────────────────────────
class UserCreate(PydanticBase):
    username: str
    email: str


class UserResponse(PydanticBase):
    id: int
    username: str
    email: str
    is_active: bool


class UserUpdate(PydanticBase):
    email: Optional[str] = None
    is_active: Optional[bool] = None


# ── DB 의존성 주입 ───────────────────────────────────
def get_db():
    """요청별 DB 연결 관리 (Depends 패턴)."""
    if db.is_closed():
        db.connect()
    try:
        yield db
    finally:
        if not db.is_closed():
            db.close()


# ── 미들웨어로 DB 연결 관리 ──────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    db.connect()
    db.create_tables(ALL_TABLES)
    yield
    db.close()


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def db_session_middleware(request, call_next):
    """미들웨어로 요청마다 DB 연결 open/close."""
    if db.is_closed():
        db.connect(reuse_if_open=True)
    try:
        response = await call_next(request)
    finally:
        if not db.is_closed():
            db.close()
    return response


# ── API 엔드포인트 ───────────────────────────────────
@app.post("/users", response_model=UserResponse)
def create_user(user_data: UserCreate, _db=Depends(get_db)):
    user = User.create(username=user_data.username, email=user_data.email)
    return model_to_dict(user, exclude=[User.created_at])


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, _db=Depends(get_db)):
    try:
        user = User.get_by_id(user_id)
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    return model_to_dict(user, exclude=[User.created_at])


@app.get("/users", response_model=list[UserResponse])
def list_users(_db=Depends(get_db)):
    users = User.select()
    return [model_to_dict(u, exclude=[User.created_at]) for u in users]


@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, _db=Depends(get_db)):
    try:
        user = User.get_by_id(user_id)
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

    if user_data.email is not None:
        user.email = user_data.email
    if user_data.is_active is not None:
        user.is_active = user_data.is_active
    user.save()
    return model_to_dict(user, exclude=[User.created_at])


@app.delete("/users/{user_id}")
def delete_user(user_id: int, _db=Depends(get_db)):
    try:
        user = User.get_by_id(user_id)
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    user.delete_instance()
    return {"deleted": True}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
