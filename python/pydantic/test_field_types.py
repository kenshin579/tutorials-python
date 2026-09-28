"""필드 타입과 제약조건 - Field, Annotated, 커스텀 타입"""

from typing import Annotated

import pytest
from pydantic import BaseModel, EmailStr, Field, HttpUrl, ValidationError


class TestFieldConstraints:
    """Field 제약조건"""

    def test_string_constraints(self):
        """문자열 길이 제약"""

        class Username(BaseModel):
            name: str = Field(min_length=2, max_length=20)

        user = Username(name="홍길동")
        assert user.name == "홍길동"

        with pytest.raises(ValidationError):
            Username(name="")  # min_length 위반

        with pytest.raises(ValidationError):
            Username(name="a" * 21)  # max_length 위반

    def test_numeric_constraints(self):
        """숫자 범위 제약"""

        class Score(BaseModel):
            value: int = Field(gt=0, le=100)

        score = Score(value=85)
        assert score.value == 85

        with pytest.raises(ValidationError):
            Score(value=0)  # gt=0 위반 (0 초과여야 함)

        with pytest.raises(ValidationError):
            Score(value=101)  # le=100 위반

    def test_default_and_alias(self):
        """기본값과 별칭 설정"""

        class Config(BaseModel):
            debug_mode: bool = Field(default=False, alias="debugMode")

        # 별칭으로 생성
        config = Config(debugMode=True)
        assert config.debug_mode is True

        # 기본값 사용
        config2 = Config()
        assert config2.debug_mode is False

    def test_annotated_pattern(self):
        """Annotated 패턴 (Python 3.9+)"""

        PositiveInt = Annotated[int, Field(ge=0)]
        NonEmptyStr = Annotated[str, Field(min_length=1)]

        class Product(BaseModel):
            name: NonEmptyStr
            price: PositiveInt
            quantity: PositiveInt

        product = Product(name="노트북", price=1500000, quantity=10)
        assert product.price == 1500000

        with pytest.raises(ValidationError):
            Product(name="", price=100, quantity=1)  # 빈 문자열

        with pytest.raises(ValidationError):
            Product(name="노트북", price=-1, quantity=1)  # 음수

    def test_field_description_and_examples(self):
        """Field에 설명과 예시 추가"""

        class ApiKey(BaseModel):
            key: str = Field(
                min_length=32,
                max_length=64,
                description="API 인증 키",
                examples=["abc123def456ghi789jkl012mno345pq"],
            )

        schema = ApiKey.model_json_schema()
        assert schema["properties"]["key"]["description"] == "API 인증 키"


class TestCustomTypes:
    """커스텀 타입 (EmailStr, HttpUrl 등)"""

    def test_email_str(self):
        """이메일 검증"""

        class Contact(BaseModel):
            email: EmailStr

        contact = Contact(email="user@example.com")
        assert contact.email == "user@example.com"

        with pytest.raises(ValidationError):
            Contact(email="not-an-email")

    def test_http_url(self):
        """URL 검증"""

        class Website(BaseModel):
            url: HttpUrl

        site = Website(url="https://example.com")
        assert str(site.url) == "https://example.com/"

        with pytest.raises(ValidationError):
            Website(url="not-a-url")

    def test_optional_fields(self):
        """Optional 필드"""

        class Profile(BaseModel):
            name: str
            bio: str | None = None
            age: int | None = None

        profile = Profile(name="홍길동")
        assert profile.bio is None
        assert profile.age is None

        profile2 = Profile(name="홍길동", bio="개발자", age=30)
        assert profile2.bio == "개발자"

    def test_literal_type(self):
        """Literal 타입으로 허용 값 제한"""
        from typing import Literal

        class Order(BaseModel):
            status: Literal["pending", "confirmed", "shipped", "delivered"]

        order = Order(status="confirmed")
        assert order.status == "confirmed"

        with pytest.raises(ValidationError):
            Order(status="cancelled")  # 허용되지 않은 값
