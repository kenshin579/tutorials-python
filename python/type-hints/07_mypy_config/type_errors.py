"""의도적 타입 에러 예제 — mypy 에러 메시지 시연용

이 파일은 mypy 실행 시 에러를 발생시키도록 의도적으로 잘못된 타입을 사용한다.
블로그에서 mypy 에러 메시지 읽는 방법을 설명할 때 사용.
"""


# 에러 1: 타입 불일치 (Incompatible types)
def add(a: int, b: int) -> int:
    return a + b


result: str = add(1, 2)  # type: ignore[assignment]  # error: Incompatible types in assignment


# 에러 2: 인자 타입 불일치
def greet(name: str) -> str:
    return f"Hello, {name}!"


greet(42)  # type: ignore[arg-type]  # error: Argument 1 has incompatible type "int"


# 에러 3: Optional 체크 누락
def find(items: list[str], target: str) -> str | None:
    if target in items:
        return target
    return None


value = find(["a", "b"], "a")
print(value.upper())  # type: ignore[union-attr]  # error: Item "None" has no attribute "upper"

# 올바른 방법:
if value is not None:
    print(value.upper())  # OK


# 에러 4: 반환 타입 누락
def compute(x: int):  # type: ignore[no-untyped-def]  # error: missing return type
    return x * 2
