"""클래스 기반 Context Manager: __enter__ / __exit__ 직접 구현"""


# 1. 기본 Context Manager
class ManagedResource:
    """리소스 획득/해제를 관리하는 기본 Context Manager"""

    def __init__(self, name: str):
        self.name = name
        print(f"  __init__: {name} 생성")

    def __enter__(self):
        print(f"  __enter__: {self.name} 획득")
        return self  # as 절에 바인딩되는 값

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"  __exit__: {self.name} 해제 (exc_type={exc_type})")
        return False  # False: 예외 전파, True: 예외 억제

    def do_work(self):
        print(f"  {self.name}으로 작업 수행")


# 2. 예외 억제 Context Manager
class SuppressError:
    """__exit__에서 True 반환 시 예외가 억제됨"""

    def __init__(self, *exceptions):
        self.exceptions = exceptions

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type and issubclass(exc_type, self.exceptions):
            print(f"  예외 억제됨: {exc_type.__name__}: {exc_val}")
            return True  # 예외 억제
        return False  # 예외 전파


# 3. 연결 관리 Context Manager
class DatabaseConnection:
    """DB 연결을 시뮬레이션하는 Context Manager"""

    def __init__(self, host: str):
        self.host = host
        self.connected = False

    def __enter__(self):
        self.connected = True
        print(f"  DB 연결됨: {self.host}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connected = False
        if exc_type:
            print(f"  에러 발생, 롤백: {exc_val}")
        else:
            print("  커밋 완료")
        print(f"  DB 연결 종료: {self.host}")
        return False

    def execute(self, query: str):
        if not self.connected:
            raise RuntimeError("연결되지 않음")
        print(f"  쿼리 실행: {query}")
        return f"result of '{query}'"


if __name__ == "__main__":
    print("=== 기본 Context Manager ===")
    with ManagedResource("리소스A") as res:
        res.do_work()

    print("\n=== 예외 억제 ===")
    with SuppressError(ValueError, TypeError):
        raise ValueError("무시될 에러")
    print("  프로그램 계속 실행됨")

    print("\n=== DB 연결 (정상) ===")
    with DatabaseConnection("localhost:5432") as db:
        db.execute("SELECT * FROM users")

    print("\n=== DB 연결 (에러) ===")
    try:
        with DatabaseConnection("localhost:5432") as db:
            db.execute("INSERT INTO users VALUES (1)")
            raise RuntimeError("제약 조건 위반")
    except RuntimeError:
        print("  예외 처리됨")
