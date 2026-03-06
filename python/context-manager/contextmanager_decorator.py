"""@contextmanager 데코레이터: yield 기반 Context Manager"""

from contextlib import contextmanager


# 1. 기본 사용
@contextmanager
def managed_resource(name: str):
    """yield 전 = __enter__, yield 후 = __exit__"""
    print(f"  리소스 획득: {name}")
    try:
        yield name  # as 절에 바인딩되는 값
    finally:
        print(f"  리소스 해제: {name}")


# 2. try/finally 패턴으로 예외 안전성 확보
@contextmanager
def safe_resource():
    """try/finally로 예외 발생 시에도 정리 보장"""
    resource = {"status": "acquired"}
    print(f"  획득: {resource}")
    try:
        yield resource
    except Exception as e:
        resource["status"] = "error"
        print(f"  에러 감지: {e}")
        raise  # 예외 재발생 (억제하려면 raise 제거)
    finally:
        resource["status"] = "released"
        print(f"  해제: {resource}")


# 3. 클래스 기반 vs @contextmanager 비교
class TimerClass:
    """클래스 기반 - 8줄"""

    def __enter__(self):
        import time

        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        import time

        self.elapsed = time.perf_counter() - self.start
        print(f"  소요 시간: {self.elapsed:.4f}초")
        return False


@contextmanager
def timer(label: str = ""):
    """@contextmanager 기반 - 5줄"""
    import time

    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"  {label}: {elapsed:.4f}초")


# 4. 중첩 활용
@contextmanager
def indented_log(level: int = 0):
    """들여쓰기 로그 context manager"""
    prefix = "  " * level
    print(f"{prefix}▶ 시작")
    try:
        yield prefix
    finally:
        print(f"{prefix}◀ 종료")


if __name__ == "__main__":
    print("=== 기본 @contextmanager ===")
    with managed_resource("DB커넥션") as name:
        print(f"  작업 수행: {name}")

    print("\n=== 예외 안전성 ===")
    try:
        with safe_resource() as res:
            print(f"  작업 중: {res}")
            raise ValueError("에러 발생!")
    except ValueError:
        print("  예외 처리 완료")

    print("\n=== 시간 측정 ===")
    with timer("작업"):
        total = sum(range(1_000_000))

    print("\n=== 중첩 로그 ===")
    with indented_log(0) as p0:
        print(f"{p0}  레벨 0 작업")
        with indented_log(1) as p1:
            print(f"{p1}  레벨 1 작업")
