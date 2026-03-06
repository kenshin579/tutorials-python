"""
structlog 바인딩 - 컨텍스트 추가
"""

import structlog


def binding_example():
    """bind()로 컨텍스트 정보 추가"""
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(sort_keys=True),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )

    # 기본 로거
    logger = structlog.get_logger()

    # bind()로 컨텍스트 추가 - 새로운 로거 인스턴스 반환
    user_logger = logger.bind(user_id=123, username="kenshin")

    # 이후 모든 로그에 user_id, username이 자동 포함
    user_logger.info("프로필 조회")
    user_logger.info("설정 변경", setting="theme", value="dark")

    # 추가 바인딩
    order_logger = user_logger.bind(order_id="ORD-456")
    order_logger.info("주문 생성")
    order_logger.info("결제 처리", amount=50000)

    # unbind()로 특정 컨텍스트 제거
    clean_logger = order_logger.unbind("order_id")
    clean_logger.info("주문 컨텍스트 제거 후 로그")

    # new()로 컨텍스트 초기화
    fresh_logger = logger.new(request_id="REQ-789")
    fresh_logger.info("새로운 요청 시작")


def thread_local_binding():
    """thread-local 바인딩으로 요청 단위 컨텍스트 관리"""
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,  # contextvars 통합
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )

    logger = structlog.get_logger()

    # 요청 시작 시 컨텍스트 바인딩
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id="REQ-001",
        client_ip="10.0.0.1",
    )

    # 어디서든 같은 컨텍스트 공유
    logger.info("요청 처리 시작")
    process_business_logic(logger)
    logger.info("요청 처리 완료")


def process_business_logic(logger):
    """비즈니스 로직 - 별도 함수에서도 컨텍스트 유지"""
    logger.info("비즈니스 로직 실행 중", step="validation")
    logger.info("데이터 저장 완료", step="save")


if __name__ == "__main__":
    print("=" * 60)
    print("1. bind/unbind 예제")
    print("=" * 60)
    binding_example()

    print("\n" + "=" * 60)
    print("2. contextvars 기반 바인딩")
    print("=" * 60)
    thread_local_binding()
