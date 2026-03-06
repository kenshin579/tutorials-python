"""
비동기 컨텍스트 매니저
- @asynccontextmanager로 간결하게 작성
- DB 커넥션 풀, HTTP 세션 lifecycle 관리
- AsyncExitStack으로 동적 개수의 비동기 리소스 관리
"""

import asyncio
from contextlib import asynccontextmanager, AsyncExitStack


# ============================================================
# 1. 클래스 기반 비동기 컨텍스트 매니저
# ============================================================
class AsyncDBConnection:
    """비동기 DB 연결을 관리하는 컨텍스트 매니저."""

    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connected = False

    async def __aenter__(self):
        print(f"  [{self.db_name}] 연결 중...")
        await asyncio.sleep(0.1)  # 연결 시뮬레이션
        self.connected = True
        print(f"  [{self.db_name}] 연결 완료")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print(f"  [{self.db_name}] 연결 해제 중...")
        await asyncio.sleep(0.05)  # 해제 시뮬레이션
        self.connected = False
        print(f"  [{self.db_name}] 연결 해제 완료")
        return False  # 예외를 전파

    async def query(self, sql: str):
        if not self.connected:
            raise RuntimeError("DB에 연결되지 않음")
        await asyncio.sleep(0.05)
        return f"결과: {sql}"


async def class_based_example():
    """클래스 기반 비동기 컨텍스트 매니저 사용 예제."""
    async with AsyncDBConnection("mydb") as conn:
        result = await conn.query("SELECT * FROM users")
        print(f"  쿼리 결과: {result}")
        return result


# ============================================================
# 2. @asynccontextmanager 데코레이터
# ============================================================
@asynccontextmanager
async def http_session(base_url: str):
    """HTTP 세션을 관리하는 비동기 컨텍스트 매니저."""
    print(f"  세션 생성: {base_url}")
    session = {"base_url": base_url, "active": True}
    try:
        yield session
    finally:
        session["active"] = False
        print(f"  세션 종료: {base_url}")


@asynccontextmanager
async def db_transaction(conn_name: str):
    """DB 트랜잭션을 관리하는 비동기 컨텍스트 매니저."""
    print(f"  [{conn_name}] 트랜잭션 시작")
    committed = False
    try:
        yield conn_name
        committed = True
        print(f"  [{conn_name}] 커밋")
    except Exception as e:
        print(f"  [{conn_name}] 롤백 (에러: {e})")
        raise
    finally:
        status = "커밋됨" if committed else "롤백됨"
        print(f"  [{conn_name}] 트랜잭션 종료 ({status})")


async def decorator_based_example():
    """@asynccontextmanager 사용 예제."""
    results = []

    # HTTP 세션
    async with http_session("https://api.example.com") as session:
        print(f"  세션 상태: {session}")
        results.append(session["base_url"])

    # 트랜잭션 성공
    async with db_transaction("main-db") as conn:
        print(f"  {conn}에서 INSERT 수행")
        results.append("insert-ok")

    # 트랜잭션 실패 (롤백)
    try:
        async with db_transaction("main-db") as conn:
            raise ValueError("데이터 검증 실패")
    except ValueError:
        results.append("rollback")

    return results


# ============================================================
# 3. 중첩 컨텍스트 매니저
# ============================================================
async def nested_context_managers():
    """여러 비동기 컨텍스트 매니저를 중첩해서 사용한다."""
    async with AsyncDBConnection("primary") as primary:
        async with AsyncDBConnection("replica") as replica:
            r1 = await primary.query("INSERT INTO logs VALUES (...)")
            r2 = await replica.query("SELECT * FROM logs")
            print(f"  primary: {r1}")
            print(f"  replica: {r2}")
            return r1, r2


# ============================================================
# 4. AsyncExitStack - 동적 개수의 리소스 관리
# ============================================================
async def exit_stack_example():
    """AsyncExitStack으로 동적 개수의 리소스를 관리한다."""
    db_names = ["db-1", "db-2", "db-3"]
    results = []

    async with AsyncExitStack() as stack:
        # 동적으로 여러 DB 연결 생성
        connections = []
        for name in db_names:
            conn = await stack.enter_async_context(AsyncDBConnection(name))
            connections.append(conn)

        # 모든 연결에서 쿼리 실행
        for conn in connections:
            result = await conn.query(f"SELECT 1 FROM {conn.db_name}")
            results.append(result)
            print(f"  {conn.db_name}: {result}")

    # AsyncExitStack을 벗어나면 모든 연결이 자동 해제됨
    print(f"  모든 연결 해제 완료. 결과 수: {len(results)}")
    return results


# ============================================================
# 5. AsyncExitStack + 콜백
# ============================================================
async def exit_stack_with_callback():
    """AsyncExitStack에 정리 콜백을 등록한다."""
    cleanup_log = []

    async def async_cleanup(resource_name: str):
        print(f"  [async 정리] {resource_name}")
        cleanup_log.append(f"async:{resource_name}")

    def sync_cleanup(resource_name: str):
        print(f"  [sync 정리] {resource_name}")
        cleanup_log.append(f"sync:{resource_name}")

    async with AsyncExitStack() as stack:
        # 비동기 정리 콜백 등록
        stack.push_async_callback(async_cleanup, "캐시")
        stack.push_async_callback(async_cleanup, "세션")
        # 동기 정리 콜백 등록
        stack.callback(sync_cleanup, "로그")

        print("  리소스 사용 중...")

    # 콜백은 LIFO 순서로 실행됨
    print(f"  정리 순서: {cleanup_log}")
    return cleanup_log


if __name__ == "__main__":
    print("=== 1. 클래스 기반 컨텍스트 매니저 ===")
    asyncio.run(class_based_example())

    print("\n=== 2. @asynccontextmanager ===")
    asyncio.run(decorator_based_example())

    print("\n=== 3. 중첩 컨텍스트 매니저 ===")
    asyncio.run(nested_context_managers())

    print("\n=== 4. AsyncExitStack ===")
    asyncio.run(exit_stack_example())

    print("\n=== 5. AsyncExitStack + 콜백 ===")
    asyncio.run(exit_stack_with_callback())
