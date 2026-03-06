"""
structlog 기본 사용법 - 구조화된 로깅
"""

import structlog


# ============================================================
# 1. 기본 사용법
# ============================================================
def basic_usage():
    """structlog 기본 로깅"""
    logger = structlog.get_logger()

    logger.info("사용자 로그인", user_id=123, ip="192.168.1.1")
    logger.warning("느린 쿼리 감지", query_time_ms=1500, table="users")
    logger.error("결제 실패", order_id="ORD-001", reason="잔액 부족")


# ============================================================
# 2. 프로세서 파이프라인 구성
# ============================================================
def processor_pipeline():
    """프로세서 파이프라인으로 로그 가공"""
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,                # 로그 레벨 추가
            structlog.processors.TimeStamper(fmt="iso"),   # ISO 타임스탬프
            structlog.processors.StackInfoRenderer(),      # 스택 정보
            structlog.processors.format_exc_info,          # 예외 정보
            structlog.processors.JSONRenderer(sort_keys=True),  # JSON 출력
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )

    logger = structlog.get_logger()

    logger.info("프로세서 파이프라인 동작", action="demo", step=1)
    logger.warning("JSON으로 출력됩니다", component="pipeline")

    try:
        result = 1 / 0
    except ZeroDivisionError:
        logger.exception("예외 발생")


# ============================================================
# 3. stdlib 통합 - 기존 logging 모듈과 공존
# ============================================================
def stdlib_integration():
    """structlog을 기존 logging 모듈과 통합"""
    import logging

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
    )

    # 기존 logging 핸들러에 structlog 포맷터 적용
    formatter = structlog.stdlib.ProcessorFormatter(
        processor=structlog.dev.ConsoleRenderer(),
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG)

    # structlog 로거 사용
    logger = structlog.get_logger("myapp")
    logger.info("stdlib 통합 완료", integrated=True)
    logger.debug("기존 logging 핸들러로 출력됩니다")


if __name__ == "__main__":
    print("=" * 60)
    print("1. 기본 사용법")
    print("=" * 60)
    basic_usage()

    print("\n" + "=" * 60)
    print("2. 프로세서 파이프라인")
    print("=" * 60)
    processor_pipeline()

    print("\n" + "=" * 60)
    print("3. stdlib 통합")
    print("=" * 60)
    stdlib_integration()
