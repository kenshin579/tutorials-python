"""직렬화와 역직렬화 - model_dump, model_dump_json, model_validate, field_serializer"""

import json
from datetime import datetime

import pytest
from pydantic import BaseModel, Field, ValidationError, field_serializer


# --- 테스트용 모델 ---
class Article(BaseModel):
    title: str
    content: str
    author: str = Field(alias="authorName")
    published_at: datetime
    views: int = 0
    draft: bool = True


class TestSerialization:
    """직렬화 (model → dict/JSON)"""

    def setup_method(self):
        self.article = Article(
            title="Pydantic 가이드",
            content="본문 내용...",
            authorName="홍길동",
            published_at=datetime(2024, 6, 15, 10, 30),
            views=1500,
        )

    def test_model_dump_basic(self):
        """model_dump() - dict 변환"""
        data = self.article.model_dump()

        assert isinstance(data, dict)
        assert data["title"] == "Pydantic 가이드"
        assert data["author"] == "홍길동"
        assert data["views"] == 1500
        assert data["draft"] is True

    def test_model_dump_include_exclude(self):
        """include/exclude 필터링"""
        # include: 특정 필드만 포함
        data = self.article.model_dump(include={"title", "author"})
        assert set(data.keys()) == {"title", "author"}

        # exclude: 특정 필드 제외
        data = self.article.model_dump(exclude={"content", "draft"})
        assert "content" not in data
        assert "draft" not in data

    def test_model_dump_by_alias(self):
        """by_alias=True - 별칭으로 직렬화"""
        data = self.article.model_dump(by_alias=True)

        assert "authorName" in data
        assert "author" not in data

    def test_model_dump_exclude_defaults(self):
        """기본값 필드 제외"""
        data = self.article.model_dump(exclude_defaults=True)

        # draft=True는 기본값이므로 제외
        assert "draft" not in data
        # views=1500은 기본값(0)과 다르므로 포함
        assert "views" in data

    def test_model_dump_json(self):
        """model_dump_json() - JSON 문자열 직접 변환"""
        json_str = self.article.model_dump_json()

        assert isinstance(json_str, str)
        parsed = json.loads(json_str)
        assert parsed["title"] == "Pydantic 가이드"
        # datetime은 ISO format 문자열로 변환
        assert "2024-06-15" in parsed["published_at"]

    def test_model_dump_json_indent(self):
        """JSON 들여쓰기"""
        json_str = self.article.model_dump_json(indent=2)

        assert "\n" in json_str  # 줄바꿈 포함
        assert "  " in json_str  # 들여쓰기 포함

    def test_field_serializer(self):
        """@field_serializer - 커스텀 직렬화"""

        class Event(BaseModel):
            name: str
            date: datetime

            @field_serializer("date")
            def serialize_date(self, value: datetime) -> str:
                return value.strftime("%Y년 %m월 %d일")

        event = Event(name="컨퍼런스", date=datetime(2024, 9, 15))
        data = event.model_dump()

        assert data["date"] == "2024년 09월 15일"


class TestDeserialization:
    """역직렬화 (dict/JSON → model)"""

    def test_model_validate_from_dict(self):
        """model_validate() - dict → 모델"""
        data = {
            "title": "FastAPI 입문",
            "content": "내용...",
            "authorName": "김개발",
            "published_at": "2024-03-10T09:00:00",
            "views": 300,
        }

        article = Article.model_validate(data)

        assert article.title == "FastAPI 입문"
        assert article.author == "김개발"
        assert article.published_at == datetime(2024, 3, 10, 9, 0)

    def test_model_validate_json(self):
        """model_validate_json() - JSON 문자열 → 모델 직접 변환"""
        json_str = '{"title": "테스트", "content": "본문", "authorName": "작성자", "published_at": "2024-01-01T00:00:00"}'

        article = Article.model_validate_json(json_str)

        assert article.title == "테스트"
        assert article.author == "작성자"

    def test_strict_mode(self):
        """strict=True - 자동 타입 변환 비활성화"""

        class StrictModel(BaseModel):
            count: int
            active: bool

        # 일반 모드: 문자열 "123"이 int로 변환됨
        normal = StrictModel.model_validate({"count": "123", "active": "true"})
        assert normal.count == 123

        # 엄격 모드: 문자열 → int 변환 거부
        with pytest.raises(ValidationError):
            StrictModel.model_validate(
                {"count": "123", "active": True}, strict=True
            )

    def test_roundtrip_serialization(self):
        """직렬화 → 역직렬화 왕복 테스트"""
        original = Article(
            title="왕복 테스트",
            content="내용",
            authorName="테스터",
            published_at=datetime(2024, 7, 1, 12, 0),
            views=42,
            draft=False,
        )

        # model → JSON (by_alias) → model
        json_str = original.model_dump_json(by_alias=True)
        restored = Article.model_validate_json(json_str)

        assert restored.title == original.title
        assert restored.author == original.author
        assert restored.published_at == original.published_at
        assert restored.views == original.views
        assert restored.draft == original.draft
