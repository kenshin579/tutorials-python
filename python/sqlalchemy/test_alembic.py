"""Alembic 마이그레이션 - 기본 흐름 테스트

Alembic은 별도의 CLI 도구로, 실제 사용은 다음과 같다:

    # 초기화
    alembic init migrations

    # 마이그레이션 생성 (모델 변경 감지)
    alembic revision --autogenerate -m "add users table"

    # 마이그레이션 적용
    alembic upgrade head

    # 롤백
    alembic downgrade -1

    # 현재 버전 확인
    alembic current

이 테스트에서는 Alembic의 프로그래밍 API를 사용하여
마이그레이션 기본 동작을 검증한다.
"""

from sqlalchemy import String, create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class UserV1(Base):
    """초기 모델"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100))


class TestAlembicConcept:
    """Alembic 마이그레이션 개념 테스트"""

    def setup_method(self):
        self.engine = create_engine("sqlite:///:memory:")

    def teardown_method(self):
        Base.metadata.drop_all(self.engine)

    def test_initial_migration(self):
        """초기 테이블 생성 (alembic upgrade head 시뮬레이션)"""
        # create_all은 Alembic의 upgrade head와 유사
        Base.metadata.create_all(self.engine)

        inspector = inspect(self.engine)
        tables = inspector.get_table_names()
        assert "users" in tables

        columns = {col["name"] for col in inspector.get_columns("users")}
        assert columns == {"id", "name", "email"}

    def test_add_column_migration(self):
        """컬럼 추가 마이그레이션 시뮬레이션"""
        Base.metadata.create_all(self.engine)

        # Alembic에서는 op.add_column()으로 처리
        # 여기서는 직접 ALTER TABLE로 시뮬레이션
        with self.engine.connect() as conn:
            conn.execute(text("ALTER TABLE users ADD COLUMN age INTEGER"))
            conn.commit()

        inspector = inspect(self.engine)
        columns = {col["name"] for col in inspector.get_columns("users")}
        assert "age" in columns

    def test_migration_data_preservation(self):
        """마이그레이션 시 기존 데이터 보존"""
        Base.metadata.create_all(self.engine)

        # 기존 데이터 삽입
        with self.engine.connect() as conn:
            conn.execute(
                text("INSERT INTO users (name, email) VALUES (:name, :email)"),
                {"name": "홍길동", "email": "hong@example.com"},
            )
            conn.commit()

        # 컬럼 추가 (마이그레이션)
        with self.engine.connect() as conn:
            conn.execute(text("ALTER TABLE users ADD COLUMN phone VARCHAR(20)"))
            conn.commit()

        # 기존 데이터가 보존되었는지 확인
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT name, email, phone FROM users")).fetchone()
            assert result[0] == "홍길동"
            assert result[1] == "hong@example.com"
            assert result[2] is None  # 새 컬럼은 NULL

    def test_alembic_env_config(self):
        """Alembic env.py 설정 패턴 확인

        실제 env.py에서는 다음과 같이 설정:

        from myapp.models import Base
        target_metadata = Base.metadata

        def run_migrations_online():
            connectable = engine_from_config(config.get_section(...))
            with connectable.connect() as connection:
                context.configure(
                    connection=connection,
                    target_metadata=target_metadata,
                )
                with context.begin_transaction():
                    context.run_migrations()
        """
        # Base.metadata에 모델 정보가 포함되어 있음을 확인
        assert "users" in Base.metadata.tables
        assert len(Base.metadata.tables["users"].columns) >= 3
