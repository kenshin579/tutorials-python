"""비동기 세션 - AsyncSession + aiosqlite"""

import pytest
from sqlalchemy import String, select
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class AsyncUser(Base):
    __tablename__ = "async_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)

    def __repr__(self) -> str:
        return f"AsyncUser(id={self.id}, name={self.name!r})"


class TestAsyncSession:
    """AsyncSession을 사용한 비동기 CRUD"""

    @pytest.fixture(autouse=True)
    async def setup_engine(self):
        self.engine = create_async_engine("sqlite+aiosqlite:///:memory:")
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await self.engine.dispose()

    async def test_async_create(self):
        """비동기 Create"""
        async with AsyncSession(self.engine) as session:
            user = AsyncUser(name="홍길동", email="hong@example.com")
            session.add(user)
            await session.commit()
            await session.refresh(user)

            assert user.id is not None

    async def test_async_read(self):
        """비동기 Read"""
        async with AsyncSession(self.engine) as session:
            session.add(AsyncUser(name="홍길동", email="hong@example.com"))
            await session.commit()

        async with AsyncSession(self.engine) as session:
            stmt = select(AsyncUser).where(AsyncUser.name == "홍길동")
            result = await session.execute(stmt)
            user = result.scalars().first()

            assert user is not None
            assert user.email == "hong@example.com"

    async def test_async_update(self):
        """비동기 Update"""
        async with AsyncSession(self.engine) as session:
            user = AsyncUser(name="홍길동", email="hong@example.com")
            session.add(user)
            await session.commit()
            await session.refresh(user)
            user_id = user.id

        async with AsyncSession(self.engine) as session:
            user = await session.get(AsyncUser, user_id)
            user.name = "홍길동(수정)"
            await session.commit()

        async with AsyncSession(self.engine) as session:
            user = await session.get(AsyncUser, user_id)
            assert user.name == "홍길동(수정)"

    async def test_async_delete(self):
        """비동기 Delete"""
        async with AsyncSession(self.engine) as session:
            user = AsyncUser(name="홍길동", email="hong@example.com")
            session.add(user)
            await session.commit()
            await session.refresh(user)
            user_id = user.id

        async with AsyncSession(self.engine) as session:
            user = await session.get(AsyncUser, user_id)
            await session.delete(user)
            await session.commit()

        async with AsyncSession(self.engine) as session:
            user = await session.get(AsyncUser, user_id)
            assert user is None

    async def test_async_multiple_operations(self):
        """비동기 여러 작업 연속 실행"""
        async with AsyncSession(self.engine) as session:
            users = [
                AsyncUser(name="김철수", email="kim@example.com"),
                AsyncUser(name="이영희", email="lee@example.com"),
                AsyncUser(name="박민수", email="park@example.com"),
            ]
            session.add_all(users)
            await session.commit()

        async with AsyncSession(self.engine) as session:
            result = await session.execute(select(AsyncUser).order_by(AsyncUser.name))
            all_users = result.scalars().all()

            assert len(all_users) == 3
            names = [u.name for u in all_users]
            assert "김철수" in names
