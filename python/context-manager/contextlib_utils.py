"""contextlib 유틸리티: suppress, redirect_stdout, closing, nullcontext"""

import io
from contextlib import closing, nullcontext, redirect_stderr, redirect_stdout, suppress


# 1. suppress - 특정 예외 무시
def suppress_demo():
    """suppress()로 특정 예외를 깔끔하게 무시"""
    # suppress 사용
    with suppress(FileNotFoundError):
        open("/nonexistent/file.txt")
    print("  FileNotFoundError 무시됨, 프로그램 계속")

    # suppress 없이 동일 코드
    try:
        open("/nonexistent/file.txt")
    except FileNotFoundError:
        pass

    # 여러 예외 타입 지정 가능
    with suppress(FileNotFoundError, PermissionError):
        open("/nonexistent/file.txt")


# 2. redirect_stdout / redirect_stderr
def redirect_demo():
    """stdout/stderr를 다른 곳으로 리다이렉트"""
    # stdout을 StringIO로 캡처
    f = io.StringIO()
    with redirect_stdout(f):
        print("이 출력은 캡처됨")

    captured = f.getvalue()
    print(f"  캡처된 내용: {captured.strip()!r}")

    # stderr 리다이렉트
    err = io.StringIO()
    with redirect_stderr(err):
        import sys

        print("에러 메시지", file=sys.stderr)

    print(f"  캡처된 stderr: {err.getvalue().strip()!r}")


# 3. closing - close() 메서드 자동 호출
class Resource:
    """close() 메서드는 있지만 context manager 프로토콜은 없는 객체"""

    def __init__(self, name):
        self.name = name
        self.closed = False

    def close(self):
        self.closed = True
        print(f"  {self.name}.close() 호출됨")

    def read(self):
        return f"{self.name}의 데이터"


def closing_demo():
    """closing()으로 close() 메서드 자동 호출 보장"""
    with closing(Resource("레거시API")) as res:
        data = res.read()
        print(f"  읽은 데이터: {data}")
    print(f"  closed={res.closed}")


# 4. nullcontext - 조건부 context manager
def nullcontext_demo():
    """nullcontext()로 조건부 context manager 적용"""

    def process(data, use_timer=False):
        from contextlib import contextmanager

        @contextmanager
        def timer():
            import time

            start = time.perf_counter()
            try:
                yield
            finally:
                print(f"  소요: {time.perf_counter() - start:.4f}초")

        cm = timer() if use_timer else nullcontext()
        with cm:
            result = sum(data)
        return result

    print("  타이머 없이:")
    process(range(100), use_timer=False)

    print("  타이머 사용:")
    process(range(1_000_000), use_timer=True)


if __name__ == "__main__":
    print("=== suppress ===")
    suppress_demo()

    print("\n=== redirect_stdout / redirect_stderr ===")
    redirect_demo()

    print("\n=== closing ===")
    closing_demo()

    print("\n=== nullcontext ===")
    nullcontext_demo()
