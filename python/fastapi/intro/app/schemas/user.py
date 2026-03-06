from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=2, max_length=50, examples=["frank"])
    email: str = Field(examples=["frank@example.com"])
    full_name: str | None = Field(default=None, examples=["Frank Oh"])


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=2, max_length=50)
    email: str | None = None
    full_name: str | None = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str | None = None
