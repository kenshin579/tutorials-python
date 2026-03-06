"""비동기 Context Manager: async with, asynccontextmanager, AsyncExitStack"""

import asyncio
from contextlib import AsyncExitStack, asynccontextmanager


# 1. 클래스 기반 비동기 Context Manager
class AsyncDBConnection:
    """__aenter__ / __aexit__ 프로토콜"""

    def __init__(self, host: str):
        self.host = host
        self.connected = False

    async def __aenter__(self):
        await asyncio.sleep(0.01)  # 연결 시뮬레이션
        self.connected = True
        print(f"  [async] DB 연결: {self.host}")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await asyncio.sleep(0.01)  # 종료 시뮬레이션
        self.connected = False
        print(f"  [async] DB 종료: {self.host}")
        return False

    async def query(self, sql: str):
        if not self.connected:
            raise RuntimeError("연결되지 않음")
        await asyncio.sleep(0.01)
        return f"result: {sql}"


# 2. @asynccontextmanager 데코레이터
@asynccontextmanager
async def async_http_session(base_url: str):
    """비동기 HTTP 세션 시뮬레이션"""
    print(f"  [async] 세션 열기: {base_url}")
    session = {"base_url": base_url, "active": True}
    try:
        yield session
    finally:
        session["active"] = False
        print(f"  [async] 세션 닫기: {base_url}")


# 3. AsyncExitStack
async def async_exit_stack_demo():
    """AsyncExitStack으로 동적 비동기 리소스 관리"""
    hosts = ["db1:5432", "db2:5432"]

    async with AsyncExitStack() as stack:
        connections = []
        for host in hosts:
            conn = await stack.enter_async_context(AsyncDBConnection(host))
            connections.append(conn)

        for conn in connections:
            result = await conn.query("SELECT 1")
            print(f"  {conn.host} → {result}")


async def main():
    # 클래스 기반
    print("=== 클래스 기반 비동기 Context Manager ===")
    async with AsyncDBConnection("localhost:5432") as db:
        result = await db.query("SELECT * FROM users")
        print(f"  결과: {result}")

    # @asynccontextmanager
    print("\n=== @asynccontextmanager ===")
    async with async_http_session("https://api.example.com") as session:
        print(f"  세션 상태: {session}")

    # AsyncExitStack
    print("\n=== AsyncExitStack ===")
    await async_exit_stack_demo()


if __name__ == "__main__":
    asyncio.run(main())
