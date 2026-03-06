"""
loguru 고급 기능 - @logger.catch, lazy, InterceptHandler
"""

import logging
import sys

from loguru import logger


# ============================================================
# 1. @logger.catch - 예외 자동 로깅
# ============================================================
def catch_decorator_example():
    """@logger.catch로 예외 자동 캡처"""

    @logger.catch
    def divide(a, b):
        return a / b

    # 정상 동작
    result = divide(10, 2)
    logger.info(f"10 / 2 = {result}")

    # 예외 발생 → 자동으로 로깅됨 (프로그램 중단 없음)
    divide(10, 0)


# ============================================================
# 2. logger.opt - 고급 옵션
# ============================================================
def opt_example():
    """logger.opt()으로 세밀한 제어"""
    # lazy=True: 지연 평가 (로그 레벨에 따라 평가 여부 결정)
    def expensive_computation():
        logger.info("비용이 큰 연산 실행됨")
        return sum(range(1000000))

    logger.opt(lazy=True).debug(
        "결과: {result}",
        result=expensive_computation,  # 함수 자체를 전달 (호출 아님)
    )

    # depth: 호출 스택 깊이 조정
    def wrapper():
        logger.opt(depth=1).info("wrapper를 호출한 곳의 위치 정보 표시")

    wrapper()

    # record: 로그 레코드 접근
    logger.opt(record=True).info("프로세스 ID: {record[process].id}")

    # exception: 예외 정보 포함
    try:
        raise ValueError("테스트 에러")
    except ValueError:
        logger.opt(exception=True).error("예외 정보 포함 로그")


# ============================================================
# 3. InterceptHandler - 기존 logging 모듈과 통합
# ============================================================
class InterceptHandler(logging.Handler):
    """표준 logging 모듈의 로그를 loguru로 리다이렉트"""

    def emit(self, record: logging.LogRecord) -> None:
        # loguru 레벨 매핑
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # 호출 위치 추적
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def intercept_handler_example():
    """InterceptHandler로 모든 로그를 loguru로 통합"""
    # 기존 logging 핸들러를 InterceptHandler로 교체
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    # 기존 logging 모듈 사용 → loguru로 출력됨
    std_logger = logging.getLogger("legacy_module")
    std_logger.info("표준 logging으로 남긴 로그 → loguru로 출력")
    std_logger.warning("경고도 loguru 포맷으로 출력됩니다")

    # loguru 직접 사용
    logger.info("loguru 직접 사용 로그")

    # 서드파티 라이브러리 로그도 통합됨
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.info("uvicorn 로그도 loguru로 통합")


# ============================================================
# 4. 구조화된 로깅 (serialize)
# ============================================================
def structured_logging():
    """loguru에서 JSON 형식 로깅"""
    logger.remove()
    logger.add(sys.stdout, serialize=True)  # JSON 출력

    logger.info("JSON 로그", user_id=123, action="login")
    logger.warning("경고 JSON 로그", component="auth")

    # 복원
    logger.remove()
    logger.add(sys.stdout, colorize=True)


if __name__ == "__main__":
    print("=" * 60)
    print("1. @logger.catch 데코레이터")
    print("=" * 60)
    catch_decorator_example()

    print("\n" + "=" * 60)
    print("2. logger.opt 고급 옵션")
    print("=" * 60)
    opt_example()

    print("\n" + "=" * 60)
    print("3. InterceptHandler - logging 통합")
    print("=" * 60)
    intercept_handler_example()

    print("\n" + "=" * 60)
    print("4. 구조화된 로깅 (JSON)")
    print("=" * 60)
    structured_logging()
