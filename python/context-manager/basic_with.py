"""with 문의 기본 동작 원리"""

import os
import tempfile


# 1. with 문 기본 사용
def basic_file_with():
    """with 문으로 파일 열기 - 자동으로 close() 호출"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("hello world")
        tmpfile = f.name
        print(f"파일 열림: {f.name}, closed={f.closed}")

    print(f"with 블록 종료 후: closed={f.closed}")
    os.unlink(tmpfile)


# 2. as 절이 받는 값 = __enter__의 반환값
def as_clause_demo():
    """as 절에 바인딩되는 값은 __enter__()의 반환값"""
    # open()의 __enter__는 self(파일 객체)를 반환
    with tempfile.NamedTemporaryFile(mode="w") as f:
        print(f"type: {type(f).__name__}")

    # 반환값이 None인 경우도 있음
    # suppress()의 __enter__는 self를 반환하지만 보통 무시


# 3. with 문 없이 수동 관리 (비교용)
def manual_resource_management():
    """try/finally로 수동 리소스 관리 - with 문이 이를 대체"""
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False)
    tmpfile = f.name
    try:
        f.write("manual management")
        print(f"수동 관리: {f.name}")
    finally:
        f.close()
        print(f"finally에서 close: closed={f.closed}")
    os.unlink(tmpfile)


# 4. with 문의 실행 흐름
def execution_flow():
    """with 문의 단계별 실행 흐름 시연"""

    class Tracer:
        def __enter__(self):
            print("  1. __enter__() 호출")
            return "리소스 객체"

        def __exit__(self, exc_type, exc_val, exc_tb):
            print(f"  3. __exit__() 호출 (exc_type={exc_type})")
            return False

    print("=== 정상 실행 ===")
    with Tracer() as resource:
        print(f"  2. with 블록 실행 (resource={resource})")

    print("\n=== 예외 발생 시 ===")
    try:
        with Tracer() as resource:
            print(f"  2. with 블록 실행 (resource={resource})")
            raise ValueError("테스트 에러")
    except ValueError:
        print("  4. 예외 전파됨")


if __name__ == "__main__":
    print("=== with 문 기본 사용 ===")
    basic_file_with()

    print("\n=== as 절 반환값 ===")
    as_clause_demo()

    print("\n=== 수동 관리 비교 ===")
    manual_resource_management()

    print("\n=== 실행 흐름 ===")
    execution_flow()
