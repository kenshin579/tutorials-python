"""BaseModel 기본 - 모델 정의, 검증, 메타데이터, JSON Schema"""

import pytest
from pydantic import BaseModel, ValidationError


# --- 기본 모델 정의 ---
class User(BaseModel):
    name: str
    age: int
    email: str


class TestBaseModel:
    """BaseModel 기본 사용법"""

    def test_basic_model_creation(self):
        """기본 모델 생성 및 필드 접근"""
        user = User(name="홍길동", age=30, email="hong@example.com")

        assert user.name == "홍길동"
        assert user.age == 30
        assert user.email == "hong@example.com"

    def test_auto_type_coercion(self):
        """자동 타입 변환 - 문자열 "25"가 int 25로 변환"""
        user = User(name="홍길동", age="25", email="hong@example.com")

        assert user.age == 25
        assert isinstance(user.age, int)

    def test_validation_error(self):
        """유효하지 않은 데이터 → ValidationError 발생"""
        with pytest.raises(ValidationError) as exc_info:
            User(name="홍길동", age="not_a_number", email="hong@example.com")

        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "int_parsing"

    def test_missing_required_field(self):
        """필수 필드 누락 시 ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            User(name="홍길동")

        error_fields = {e["loc"][0] for e in exc_info.value.errors()}
        assert "age" in error_fields
        assert "email" in error_fields

    def test_model_fields(self):
        """model_fields로 필드 메타데이터 접근"""
        fields = User.model_fields

        assert "name" in fields
        assert "age" in fields
        assert "email" in fields
        assert fields["name"].annotation is str
        assert fields["age"].annotation is int

    def test_model_json_schema(self):
        """JSON Schema 자동 생성"""
        schema = User.model_json_schema()

        assert schema["title"] == "User"
        assert schema["type"] == "object"
        assert "name" in schema["properties"]
        assert "age" in schema["properties"]
        assert schema["properties"]["age"]["type"] == "integer"
        assert set(schema["required"]) == {"name", "age", "email"}

    def test_model_fields_set(self):
        """명시적으로 설정된 필드 추적"""

        class Profile(BaseModel):
            name: str
            bio: str = "소개 없음"
            active: bool = True

        profile = Profile(name="홍길동", bio="개발자")

        assert profile.model_fields_set == {"name", "bio"}
        assert "active" not in profile.model_fields_set
