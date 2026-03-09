"""네이밍 컨벤션에서의 언더스코어 예제"""

# 3.1 선행 단일 언더스코어 (_name) - "내부 사용" 컨벤션
# 외부에서 접근 가능하지만, "내부 구현"임을 나타낸다


class ApiClient:
    """API 클라이언트 예제 - 내부 메서드와 공개 메서드 구분"""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self._session_token = None  # 내부 사용 변수

    def connect(self) -> str:
        """공개 메서드: 연결을 수행한다."""
        self._session_token = self._generate_token()
        return f"Connected to {self.base_url}"

    def _generate_token(self) -> str:
        """내부 메서드: 외부에서 호출하지 말 것을 권장한다."""
        return "secret-token-123"


# __all__과의 관계 - 이 모듈에서 export할 이름을 명시
__all__ = ["ApiClient", "public_function"]


def public_function() -> str:
    return "I am public"


def _private_function() -> str:
    """_로 시작하면 from module import * 시 제외된다."""
    return "I am private"


# 3.2 후행 단일 언더스코어 (name_) - 키워드 충돌 방지
def create_element(type_: str, class_: str = "") -> dict:
    """Python 키워드와 충돌을 피하기 위해 후행 언더스코어를 사용한다.

    PEP 8: "single trailing underscore by convention to avoid conflicts
    with Python keyword"
    """
    return {"type": type_, "class": class_}
