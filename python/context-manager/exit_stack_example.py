"""ExitStack: 동적 개수의 Context Manager 관리"""

import os
import tempfile
from contextlib import ExitStack, contextmanager


# 1. 동적 파일 열기
def dynamic_files():
    """ExitStack으로 동적 개수의 파일 관리"""
    # 임시 파일 생성
    tmp_files = []
    for i in range(3):
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=f"_{i}.txt", delete=False, prefix="test_"
        )
        f.write(f"content {i}")
        f.close()
        tmp_files.append(f.name)

    try:
        with ExitStack() as stack:
            files = [stack.enter_context(open(f)) for f in tmp_files]
            for f in files:
                print(f"  {os.path.basename(f.name)}: {f.read()}")
        # ExitStack 종료 시 모든 파일 자동 닫힘
        print(f"  모든 파일 닫힘: {[f.closed for f in files]}")
    finally:
        for f in tmp_files:
            os.unlink(f)


# 2. callback 등록
def callback_demo():
    """ExitStack에 cleanup 콜백 등록"""

    def cleanup(name):
        print(f"  cleanup: {name}")

    with ExitStack() as stack:
        stack.callback(cleanup, "첫 번째")
        stack.callback(cleanup, "두 번째")
        stack.callback(cleanup, "세 번째")
        print("  작업 수행 중...")
    # LIFO 순서로 콜백 실행


# 3. LIFO 순서 확인
def lifo_order():
    """cleanup 순서가 LIFO(후입선출)임을 확인"""

    @contextmanager
    def numbered(n):
        print(f"  enter: {n}")
        try:
            yield n
        finally:
            print(f"  exit: {n}")

    with ExitStack() as stack:
        for i in range(1, 4):
            stack.enter_context(numbered(i))
        print("  --- 모든 리소스 획득 완료 ---")


# 4. 조건부 context manager 관리
def conditional_resources():
    """조건에 따라 동적으로 context manager 추가"""

    @contextmanager
    def optional_resource(name):
        print(f"  {name} 획득")
        try:
            yield name
        finally:
            print(f"  {name} 해제")

    resources = ["DB", "Cache", "Queue"]
    enabled = {"DB": True, "Cache": True, "Queue": False}

    with ExitStack() as stack:
        active = []
        for name in resources:
            if enabled.get(name, False):
                res = stack.enter_context(optional_resource(name))
                active.append(res)
        print(f"  활성 리소스: {active}")


if __name__ == "__main__":
    print("=== 동적 파일 열기 ===")
    dynamic_files()

    print("\n=== callback 등록 ===")
    callback_demo()

    print("\n=== LIFO 순서 ===")
    lifo_order()

    print("\n=== 조건부 리소스 ===")
    conditional_resources()
