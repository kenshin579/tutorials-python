"""실전 패턴: 파일 처리, 무한 시퀀스, 데이터 파이프라인"""

import os
import tempfile
from typing import Generator, Iterable, Iterator


# 1. 대용량 파일 처리 파이프라인
def read_lines(filepath: str) -> Generator[str, None, None]:
    """파일을 라인 단위로 읽는 Generator"""
    with open(filepath) as f:
        for line in f:
            yield line.strip()


def filter_non_empty(lines: Iterable[str]) -> Generator[str, None, None]:
    """빈 줄 필터링"""
    for line in lines:
        if line:
            yield line


def to_upper(lines: Iterable[str]) -> Generator[str, None, None]:
    """대문자 변환"""
    for line in lines:
        yield line.upper()


def file_pipeline(filepath: str) -> list[str]:
    """파이프라인 조합: 읽기 → 필터 → 변환"""
    lines = read_lines(filepath)
    non_empty = filter_non_empty(lines)
    uppered = to_upper(non_empty)
    return list(uppered)


# 2. 무한 시퀀스
def fibonacci() -> Generator[int, None, None]:
    """피보나치 수열 (무한)"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def id_generator(prefix: str = "ID") -> Generator[str, None, None]:
    """고유 ID 생성기 (무한)"""
    n = 1
    while True:
        yield f"{prefix}-{n:06d}"
        n += 1


# 3. 데이터 파이프라인 체이닝
def pipe(data: Iterable, *functions) -> Iterator:
    """함수 체이닝 파이프라인"""
    result = data
    for func in functions:
        result = func(result)
    return result


def double(items: Iterable[int]) -> Generator[int, None, None]:
    for x in items:
        yield x * 2


def keep_even(items: Iterable[int]) -> Generator[int, None, None]:
    for x in items:
        if x % 2 == 0:
            yield x


def take(n: int):
    """처음 n개만 가져오는 Generator 팩토리"""

    def _take(items: Iterable) -> Generator:
        for i, item in enumerate(items):
            if i >= n:
                break
            yield item

    return _take


if __name__ == "__main__":
    # 1. 파일 처리 파이프라인
    print("=== 파일 처리 파이프라인 ===")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("hello world\n\npython generator\n\ndata pipeline\n")
        tmpfile = f.name

    try:
        result = file_pipeline(tmpfile)
        print(result)
    finally:
        os.unlink(tmpfile)

    # 2. 무한 시퀀스
    print("\n=== 피보나치 (처음 10개) ===")
    fib = fibonacci()
    print([next(fib) for _ in range(10)])

    print("\n=== ID 생성기 ===")
    ids = id_generator("USR")
    print([next(ids) for _ in range(5)])

    # 3. 데이터 파이프라인
    print("\n=== 데이터 파이프라인 ===")
    data = range(1, 20)
    result = pipe(data, keep_even, double, take(5))
    print(f"keep_even → double → take(5): {list(result)}")
