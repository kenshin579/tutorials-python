"""if __name__ == "__main__": 패턴 예제

이 파일을 직접 실행하면 __name__이 "__main__"이 되고,
다른 모듈에서 import하면 __name__이 "05_main_pattern"이 된다.
"""


def greet(name: str) -> str:
    return f"Hello, {name}!"


def get_module_name() -> str:
    """현재 모듈의 __name__ 값을 반환한다."""
    return __name__


if __name__ == "__main__":
    print(f"__name__ = {__name__}")
    print(greet("World"))
