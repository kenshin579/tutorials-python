"""선언적 매핑 - DeclarativeBase, Mapped, mapped_column, 테이블 생성"""

from typing import Optional

from sqlalchemy import String, create_engine, inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# --- DeclarativeBase 정의 ---
class Base(DeclarativeBase):
    pass


# --- 모델 정의 ---
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    bio: Mapped[Optional[str]] = mapped_column(String(200), default=None)
    active: Mapped[bool] = mapped_column(default=True)

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name!r}, email={self.email!r})"


class TestDeclarativeMapping:
    """DeclarativeBase와 Mapped를 사용한 선언적 매핑"""

    def setup_method(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

    def teardown_method(self):
        Base.metadata.drop_all(self.engine)

    def test_table_created(self):
        """테이블 자동 생성 확인"""
        inspector = inspect(self.engine)
        tables = inspector.get_table_names()

        assert "users" in tables

    def test_column_types(self):
        """컬럼 타입 확인"""
        inspector = inspect(self.engine)
        columns = {col["name"]: col for col in inspector.get_columns("users")}

        assert "id" in columns
        assert "name" in columns
        assert "email" in columns
        assert "bio" in columns
        assert "active" in columns

    def test_mapped_fields(self):
        """Mapped 필드 메타데이터"""
        fields = User.__table__.columns

        assert fields["id"].primary_key
        assert fields["email"].unique
        assert fields["bio"].nullable
        assert not fields["name"].nullable  # Mapped[str]은 NOT NULL

    def test_tablename(self):
        """__tablename__ 확인"""
        assert User.__tablename__ == "users"
        assert User.__table__.name == "users"

    def test_optional_mapped_nullable(self):
        """Mapped[Optional[str]]은 nullable=True"""
        bio_col = User.__table__.columns["bio"]
        assert bio_col.nullable is True

    def test_required_mapped_not_null(self):
        """Mapped[str]은 nullable=False (NOT NULL)"""
        name_col = User.__table__.columns["name"]
        assert name_col.nullable is False
