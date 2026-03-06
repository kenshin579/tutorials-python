"""
JSON 로그 포맷 + 상관관계 ID (Correlation ID)
"""

import logging
import uuid
from contextvars import ContextVar

from pythonjsonlogger import json as jsonlogger

# 상관관계 ID를 저장할 ContextVar
correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="")


# ============================================================
# 1. JSON 포맷 로거 설정
# ============================================================
class CorrelationIdFilter(logging.Filter):
    """로그 레코드에 상관관계 ID를 추가하는 필터"""

    def filter(self, record):
        record.correlation_id = correlation_id_var.get("")
        return True


def setup_json_logger():
    """JSON 포맷 + 상관관계 ID 로거 설정"""
    logger = logging.getLogger("json_app")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    # JSON 포맷터
    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(name)s %(levelname)s %(correlation_id)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    # 상관관계 ID 필터 추가
    handler.addFilter(CorrelationIdFilter())

    logger.addHandler(handler)
    return logger


# ============================================================
# 2. 상관관계 ID 사용 예제
# ============================================================
def process_request(logger: logging.Logger):
    """요청 처리 시뮬레이션"""
    # 요청마다 고유 상관관계 ID 설정
    request_id = str(uuid.uuid4())
    correlation_id_var.set(request_id)

    logger.info("요청 수신", extra={"endpoint": "/api/users", "method": "GET"})

    # 서비스 레이어 호출
    fetch_user_data(logger)

    # 응답
    logger.info("응답 전송", extra={"status_code": 200, "duration_ms": 45})


def fetch_user_data(logger: logging.Logger):
    """서비스 레이어 - 같은 correlation_id가 자동 포함됨"""
    logger.info("DB 쿼리 실행", extra={"table": "users", "query_type": "SELECT"})
    logger.debug("캐시 확인", extra={"cache_hit": False})


# ============================================================
# 3. 실행
# ============================================================
if __name__ == "__main__":
    logger = setup_json_logger()

    print("=== 요청 1 ===")
    process_request(logger)

    print("\n=== 요청 2 ===")
    process_request(logger)

    print("\n--- 같은 correlation_id를 가진 로그끼리 묶어서 추적 가능 ---")
