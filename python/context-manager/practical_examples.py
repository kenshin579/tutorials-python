"""실전 활용 패턴: DB, 파일, 락, 임시 리소스, 시간 측정"""

import os
import tempfile
import threading
import time
from contextlib import contextmanager


# 1. DB 트랜잭션 관리
class FakeDB:
    """DB 연결 시뮬레이션"""

    def __init__(self):
        self.data = {}

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)


@contextmanager
def transaction(db: FakeDB):
    """트랜잭션 context manager - commit/rollback 자동 관리"""
    snapshot = dict(db.data)
    try:
        yield db
        print("  트랜잭션 커밋")
    except Exception as e:
        db.data = snapshot  # 롤백
        print(f"  트랜잭션 롤백: {e}")
        raise


# 2. 여러 파일 동시 처리
@contextmanager
def multi_open(*filenames, mode="r"):
    """여러 파일을 동시에 열고 자동으로 닫기"""
    files = []
    try:
        for name in filenames:
            files.append(open(name, mode))
        yield files
    finally:
        for f in files:
            f.close()


# 3. 락 관리
@contextmanager
def locked(lock: threading.Lock, timeout: float = -1):
    """타임아웃 지원 락 context manager"""
    acquired = lock.acquire(timeout=timeout)
    if not acquired:
        raise TimeoutError(f"락 획득 실패 (timeout={timeout}s)")
    try:
        yield
    finally:
        lock.release()


# 4. 임시 리소스 - 환경변수 임시 변경
@contextmanager
def temp_env(**env_vars):
    """환경변수를 임시로 변경하고 복원"""
    old_values = {}
    for key, value in env_vars.items():
        old_values[key] = os.environ.get(key)
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value
    try:
        yield
    finally:
        for key, old_value in old_values.items():
            if old_value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = old_value


# 5. 실행 시간 측정
@contextmanager
def timer(label: str = ""):
    """코드 블록의 실행 시간 측정"""
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"  {label}: {elapsed:.4f}초")


if __name__ == "__main__":
    # 1. 트랜잭션
    print("=== DB 트랜잭션 ===")
    db = FakeDB()
    with transaction(db) as d:
        d.set("user", "Alice")
    print(f"  커밋 후: {db.data}")

    print("\n  롤백 테스트:")
    try:
        with transaction(db) as d:
            d.set("user", "Bob")
            raise ValueError("에러!")
    except ValueError:
        pass
    print(f"  롤백 후: {db.data}")

    # 2. 여러 파일
    print("\n=== 여러 파일 동시 처리 ===")
    tmp1 = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False)
    tmp2 = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False)
    tmp1.write("파일1 내용")
    tmp2.write("파일2 내용")
    tmp1.close()
    tmp2.close()

    with multi_open(tmp1.name, tmp2.name) as files:
        for f in files:
            print(f"  {os.path.basename(f.name)}: {f.read()}")

    os.unlink(tmp1.name)
    os.unlink(tmp2.name)

    # 3. 락
    print("\n=== 락 관리 ===")
    lock = threading.Lock()
    with locked(lock):
        print("  락 획득 상태에서 작업")
    print("  락 해제됨")

    # 4. 환경변수
    print("\n=== 환경변수 임시 변경 ===")
    print(f"  변경 전: DEBUG={os.environ.get('DEBUG', 'unset')}")
    with temp_env(DEBUG="true", APP_MODE="test"):
        print(f"  변경 중: DEBUG={os.environ.get('DEBUG')}, APP_MODE={os.environ.get('APP_MODE')}")
    print(f"  복원 후: DEBUG={os.environ.get('DEBUG', 'unset')}")

    # 5. 시간 측정
    print("\n=== 실행 시간 측정 ===")
    with timer("sum 계산"):
        total = sum(range(1_000_000))
