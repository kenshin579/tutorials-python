"""세션 관리와 CRUD - Session, select, add, delete, flush vs commit"""

from typing import Optional

from sqlalchemy import String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    age: Mapped[Optional[int]] = mapped_column(default=None)

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name!r})"


class TestSessionCRUD:
    """Session을 사용한 CRUD 작업"""

    def setup_method(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

    def teardown_method(self):
        Base.metadata.drop_all(self.engine)

    def test_create_single(self):
        """Create - session.add()로 단일 레코드 추가"""
        with Session(self.engine) as session:
            user = User(name="홍길동", email="hong@example.com", age=30)
            session.add(user)
            session.commit()

            assert user.id is not None  # auto increment

        # 새 세션에서 확인
        with Session(self.engine) as session:
            result = session.execute(select(User)).scalars().all()
            assert len(result) == 1
            assert result[0].name == "홍길동"

    def test_create_multiple(self):
        """Create - session.add_all()로 여러 레코드 추가"""
        with Session(self.engine) as session:
            users = [
                User(name="김철수", email="kim@example.com", age=25),
                User(name="이영희", email="lee@example.com", age=28),
                User(name="박민수", email="park@example.com", age=35),
            ]
            session.add_all(users)
            session.commit()

        with Session(self.engine) as session:
            count = len(session.execute(select(User)).scalars().all())
            assert count == 3

    def test_read_select_where(self):
        """Read - select().where()로 조건 조회"""
        with Session(self.engine) as session:
            session.add_all([
                User(name="홍길동", email="hong@example.com", age=30),
                User(name="김철수", email="kim@example.com", age=25),
            ])
            session.commit()

        with Session(self.engine) as session:
            # 조건 조회
            stmt = select(User).where(User.name == "홍길동")
            user = session.execute(stmt).scalars().first()

            assert user is not None
            assert user.name == "홍길동"
            assert user.age == 30

    def test_read_get_by_id(self):
        """Read - session.get()으로 PK 조회"""
        with Session(self.engine) as session:
            user = User(name="홍길동", email="hong@example.com")
            session.add(user)
            session.commit()
            user_id = user.id

        with Session(self.engine) as session:
            found = session.get(User, user_id)

            assert found is not None
            assert found.name == "홍길동"

    def test_read_filter_multiple(self):
        """Read - 여러 조건으로 필터링"""
        with Session(self.engine) as session:
            session.add_all([
                User(name="홍길동", email="hong@example.com", age=30),
                User(name="김철수", email="kim@example.com", age=25),
                User(name="이영희", email="lee@example.com", age=35),
            ])
            session.commit()

        with Session(self.engine) as session:
            # 나이 30 이상인 사용자
            stmt = select(User).where(User.age >= 30).order_by(User.age)
            users = session.execute(stmt).scalars().all()

            assert len(users) == 2
            assert users[0].name == "홍길동"
            assert users[1].name == "이영희"

    def test_update(self):
        """Update - 객체 속성 변경 후 commit"""
        with Session(self.engine) as session:
            user = User(name="홍길동", email="hong@example.com", age=30)
            session.add(user)
            session.commit()
            user_id = user.id

        with Session(self.engine) as session:
            user = session.get(User, user_id)
            user.name = "홍길동(수정)"
            user.age = 31
            session.commit()

        with Session(self.engine) as session:
            user = session.get(User, user_id)
            assert user.name == "홍길동(수정)"
            assert user.age == 31

    def test_delete(self):
        """Delete - session.delete()"""
        with Session(self.engine) as session:
            user = User(name="홍길동", email="hong@example.com")
            session.add(user)
            session.commit()
            user_id = user.id

        with Session(self.engine) as session:
            user = session.get(User, user_id)
            session.delete(user)
            session.commit()

        with Session(self.engine) as session:
            user = session.get(User, user_id)
            assert user is None

    def test_flush_vs_commit(self):
        """flush vs commit - flush는 DB에 보내지만 트랜잭션은 유지"""
        with Session(self.engine) as session:
            user = User(name="홍길동", email="hong@example.com")
            session.add(user)

            # flush: SQL 실행하지만 트랜잭션 커밋하지 않음
            session.flush()
            assert user.id is not None  # ID가 할당됨

            # rollback하면 flush된 내용도 취소됨
            session.rollback()

        with Session(self.engine) as session:
            users = session.execute(select(User)).scalars().all()
            assert len(users) == 0  # rollback되어 데이터 없음

    def test_sessionmaker_factory(self):
        """sessionmaker - 세션 팩토리"""
        SessionLocal = sessionmaker(bind=self.engine)

        with SessionLocal() as session:
            user = User(name="홍길동", email="hong@example.com")
            session.add(user)
            session.commit()

        with SessionLocal() as session:
            users = session.execute(select(User)).scalars().all()
            assert len(users) == 1
