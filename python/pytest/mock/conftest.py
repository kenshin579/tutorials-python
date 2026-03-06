import pytest

from app.repository import User


@pytest.fixture
def sample_user() -> User:
    """공통 테스트용 사용자 데이터."""
    return User(id=1, name="Frank Oh", email="frank@example.com")


@pytest.fixture
def sample_user_dict() -> dict:
    """API 응답 형태의 사용자 데이터."""
    return {
        "id": 1,
        "name": "Frank Oh",
        "email": "frank@example.com",
        "username": "frankoh",
    }
