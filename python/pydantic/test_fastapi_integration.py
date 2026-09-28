"""FastAPI 통합 - 요청/응답 모델 분리, TestClient 검증"""

from datetime import datetime

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, EmailStr, Field


# --- 요청/응답 모델 분리 패턴 ---
class UserCreate(BaseModel):
    """회원가입 요청 모델"""

    name: str = Field(min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    """회원 응답 모델 (password 제외)"""

    id: int
    name: str
    email: EmailStr
    created_at: datetime


class UserUpdate(BaseModel):
    """회원정보 수정 요청 (모든 필드 Optional)"""

    name: str | None = None
    email: EmailStr | None = None


# --- FastAPI 앱 ---
app = FastAPI()

# 간단한 인메모리 저장소
fake_db: dict[int, dict] = {}
next_id = 1


@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    global next_id
    user_data = {
        "id": next_id,
        "name": user.name,
        "email": user.email,
        "password": user.password,  # DB에는 저장하지만
        "created_at": datetime.now(),
    }
    fake_db[next_id] = user_data
    next_id += 1
    return user_data  # response_model이 password 자동 제외


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    if user_id not in fake_db:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    return fake_db[user_id]


# --- 테스트 ---
client = TestClient(app)


class TestFastAPIIntegration:
    """FastAPI + Pydantic 통합 테스트"""

    def setup_method(self):
        fake_db.clear()
        global next_id
        next_id = 1

    def test_create_user_success(self):
        """정상적인 회원가입"""
        response = client.post(
            "/users",
            json={
                "name": "홍길동",
                "email": "hong@example.com",
                "password": "securepass123",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "홍길동"
        assert data["email"] == "hong@example.com"
        assert "password" not in data  # response_model이 제외
        assert "id" in data
        assert "created_at" in data

    def test_create_user_validation_error(self):
        """유효하지 않은 데이터 → 422 에러"""
        response = client.post(
            "/users",
            json={
                "name": "",  # min_length=1 위반
                "email": "not-email",  # 이메일 형식 위반
                "password": "short",  # min_length=8 위반
            },
        )

        assert response.status_code == 422
        errors = response.json()["detail"]
        assert len(errors) >= 2  # 여러 검증 에러

    def test_get_user_success(self):
        """회원 조회"""
        # 먼저 회원 생성
        client.post(
            "/users",
            json={
                "name": "김철수",
                "email": "kim@example.com",
                "password": "password123",
            },
        )

        response = client.get("/users/1")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "김철수"
        assert "password" not in data

    def test_get_user_not_found(self):
        """존재하지 않는 회원 → 404"""
        response = client.get("/users/999")

        assert response.status_code == 404

    def test_swagger_schema(self):
        """OpenAPI 스키마 자동 생성 확인"""
        response = client.get("/openapi.json")

        assert response.status_code == 200
        schema = response.json()
        assert "UserCreate" in schema["components"]["schemas"]
        assert "UserResponse" in schema["components"]["schemas"]

        # UserResponse에 password 필드가 없어야 함
        user_response_schema = schema["components"]["schemas"]["UserResponse"]
        assert "password" not in user_response_schema["properties"]
