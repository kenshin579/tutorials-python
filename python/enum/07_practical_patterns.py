"""실전 패턴 - 상태 머신, API 응답 코드, 설정값 관리, match/case"""

from enum import Enum, IntEnum, StrEnum


# 5.1 상태 머신
class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

    def next_status(self) -> list["OrderStatus"]:
        """현재 상태에서 전이 가능한 다음 상태 목록을 반환한다."""
        transitions = {
            OrderStatus.PENDING: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
            OrderStatus.CONFIRMED: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
            OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
            OrderStatus.DELIVERED: [],
            OrderStatus.CANCELLED: [],
        }
        return transitions[self]

    def can_transition_to(self, target: "OrderStatus") -> bool:
        return target in self.next_status()


# 5.2 API 응답 코드
class HttpCode(IntEnum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_ERROR = 500

    @property
    def category(self) -> str:
        if self.value < 200:
            return "Informational"
        elif self.value < 300:
            return "Success"
        elif self.value < 400:
            return "Redirection"
        elif self.value < 500:
            return "Client Error"
        else:
            return "Server Error"

    @property
    def is_error(self) -> bool:
        return self.value >= 400


# 5.3 설정값 관리
class Environment(StrEnum):
    DEV = "development"
    STAGING = "staging"
    PROD = "production"

    @property
    def config(self) -> dict:
        configs = {
            Environment.DEV: {"debug": True, "db": "sqlite:///dev.db", "log_level": "DEBUG"},
            Environment.STAGING: {"debug": False, "db": "postgresql://staging/db", "log_level": "INFO"},
            Environment.PROD: {"debug": False, "db": "postgresql://prod/db", "log_level": "WARNING"},
        }
        return configs[self]


# 5.4 match/case와 Enum 조합
def handle_order(status: OrderStatus) -> str:
    """match/case로 주문 상태를 처리한다."""
    match status:
        case OrderStatus.PENDING:
            return "주문 확인 중..."
        case OrderStatus.CONFIRMED:
            return "주문이 확인되었습니다."
        case OrderStatus.SHIPPED:
            return "배송 중입니다."
        case OrderStatus.DELIVERED:
            return "배송 완료!"
        case OrderStatus.CANCELLED:
            return "주문이 취소되었습니다."
