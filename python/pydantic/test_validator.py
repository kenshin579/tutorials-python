"""Validator - field_validator, model_validator"""

import pytest
from pydantic import BaseModel, ValidationError, field_validator, model_validator


class TestFieldValidator:
    """@field_validator - 단일 필드 검증/변환"""

    def test_field_validator_after(self):
        """mode='after' (기본값) - 타입 변환 후 검증"""

        class User(BaseModel):
            name: str

            @field_validator("name")
            @classmethod
            def name_must_not_be_empty(cls, v: str) -> str:
                if not v.strip():
                    raise ValueError("이름은 빈 문자열일 수 없습니다")
                return v.strip()

        user = User(name="  홍길동  ")
        assert user.name == "홍길동"  # strip 적용

        with pytest.raises(ValidationError):
            User(name="   ")

    def test_field_validator_before(self):
        """mode='before' - 타입 변환 전 검증 (raw 입력값 처리)"""

        class Price(BaseModel):
            amount: float

            @field_validator("amount", mode="before")
            @classmethod
            def parse_price_string(cls, v):
                """'₩1,000' 같은 문자열을 float로 변환"""
                if isinstance(v, str):
                    cleaned = v.replace("₩", "").replace(",", "").strip()
                    return float(cleaned)
                return v

        price = Price(amount="₩1,500,000")
        assert price.amount == 1500000.0

        price2 = Price(amount=99.9)
        assert price2.amount == 99.9

    def test_multiple_fields_validator(self):
        """여러 필드에 동일한 validator 적용"""

        class Form(BaseModel):
            first_name: str
            last_name: str

            @field_validator("first_name", "last_name")
            @classmethod
            def capitalize_name(cls, v: str) -> str:
                return v.strip().title()

        form = Form(first_name="john", last_name="doe")
        assert form.first_name == "John"
        assert form.last_name == "Doe"


class TestModelValidator:
    """@model_validator - 여러 필드 간 교차 검증"""

    def test_model_validator_after(self):
        """mode='after' - 모든 필드 검증 후 모델 레벨 검증"""

        class DateRange(BaseModel):
            start_date: str
            end_date: str

            @model_validator(mode="after")
            def check_date_order(self):
                if self.start_date >= self.end_date:
                    raise ValueError("start_date는 end_date보다 이전이어야 합니다")
                return self

        date_range = DateRange(start_date="2024-01-01", end_date="2024-12-31")
        assert date_range.start_date == "2024-01-01"

        with pytest.raises(ValidationError):
            DateRange(start_date="2024-12-31", end_date="2024-01-01")

    def test_model_validator_after_password_confirm(self):
        """비밀번호 확인 - 대표적인 교차 검증 사례"""

        class PasswordChange(BaseModel):
            password: str
            password_confirm: str

            @model_validator(mode="after")
            def passwords_match(self):
                if self.password != self.password_confirm:
                    raise ValueError("비밀번호가 일치하지 않습니다")
                return self

        valid = PasswordChange(password="secret123", password_confirm="secret123")
        assert valid.password == "secret123"

        with pytest.raises(ValidationError):
            PasswordChange(password="secret123", password_confirm="different")

    def test_model_validator_wrap(self):
        """mode='wrap' - 전체 검증 흐름 제어"""

        class FlexibleUser(BaseModel):
            name: str
            age: int

            @model_validator(mode="wrap")
            @classmethod
            def handle_string_input(cls, values, handler):
                """문자열 입력을 dict로 변환 후 검증"""
                if isinstance(values, str):
                    # "이름:나이" 형식 파싱
                    parts = values.split(":")
                    if len(parts) == 2:
                        values = {"name": parts[0], "age": int(parts[1])}
                return handler(values)

        # 일반 dict 입력
        user1 = FlexibleUser(name="홍길동", age=30)
        assert user1.name == "홍길동"

        # 문자열 입력 → wrap validator가 dict로 변환
        user2 = FlexibleUser.model_validate("김철수:25")
        assert user2.name == "김철수"
        assert user2.age == 25
