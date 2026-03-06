"""
로그 레벨 - DEBUG, INFO, WARNING, ERROR, CRITICAL
"""

import logging
import os


# ============================================================
# 1. 각 레벨별 출력
# ============================================================
def log_level_basics():
    """5가지 로그 레벨의 의미와 사용"""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)-8s [%(name)s] %(message)s",
        force=True,  # 기존 설정 덮어쓰기
    )
    logger = logging.getLogger("level_demo")

    # DEBUG(10): 개발 시 상세 디버깅 정보
    logger.debug("변수 x=42, 리스트 길이=100")

    # INFO(20): 정상 동작 확인용
    logger.info("서버가 포트 8000에서 시작되었습니다")

    # WARNING(30): 잠재적 문제 (기본 레벨)
    logger.warning("디스크 사용률이 85%%를 초과했습니다")

    # ERROR(40): 오류 발생, 기능 실패
    logger.error("데이터베이스 연결에 실패했습니다")

    # CRITICAL(50): 심각한 오류, 프로그램 종료 가능
    logger.critical("메모리 부족으로 시스템이 중단됩니다")


# ============================================================
# 2. 로거 레벨 vs 핸들러 레벨 필터링
# ============================================================
def level_filtering():
    """로거 레벨과 핸들러 레벨의 필터링 차이"""
    logger = logging.getLogger("filter_demo")
    logger.setLevel(logging.DEBUG)  # 로거: DEBUG 이상 허용
    logger.handlers.clear()

    # 핸들러 1: WARNING 이상만 출력
    handler_warning = logging.StreamHandler()
    handler_warning.setLevel(logging.WARNING)
    handler_warning.setFormatter(
        logging.Formatter("[WARNING+] %(message)s")
    )

    # 핸들러 2: DEBUG 이상 모두 출력
    handler_debug = logging.StreamHandler()
    handler_debug.setLevel(logging.DEBUG)
    handler_debug.setFormatter(
        logging.Formatter("[ALL     ] %(message)s")
    )

    logger.addHandler(handler_warning)
    logger.addHandler(handler_debug)

    print("--- 로거(DEBUG) + 핸들러(WARNING/DEBUG) 필터링 ---")
    logger.debug("DEBUG 메시지 → ALL 핸들러에서만 출력")
    logger.info("INFO 메시지 → ALL 핸들러에서만 출력")
    logger.warning("WARNING 메시지 → 두 핸들러 모두 출력")
    logger.error("ERROR 메시지 → 두 핸들러 모두 출력")


# ============================================================
# 3. 환경별 레벨 설정
# ============================================================
def environment_based_level():
    """환경 변수로 로그 레벨 동적 설정"""
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()

    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s - %(levelname)s - %(message)s",
        force=True,
    )
    logger = logging.getLogger("env_demo")

    logger.debug("이 메시지는 LOG_LEVEL=DEBUG일 때만 보입니다")
    logger.info(f"현재 로그 레벨: {log_level}")
    logger.warning("WARNING 이상은 항상 보입니다")

    print(f"\n팁: LOG_LEVEL=DEBUG python 02_log_levels.py 로 실행해보세요")


# ============================================================
# 4. 숫자 값으로 커스텀 레벨 확인
# ============================================================
def numeric_levels():
    """로그 레벨의 숫자 값"""
    levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    print("--- 로그 레벨 숫자 값 ---")
    for name, value in levels.items():
        print(f"  {name:10s} = {value}")


if __name__ == "__main__":
    print("=" * 60)
    print("1. 로그 레벨 기본")
    print("=" * 60)
    log_level_basics()

    print("\n" + "=" * 60)
    print("2. 레벨 필터링")
    print("=" * 60)
    level_filtering()

    print("\n" + "=" * 60)
    print("3. 환경별 레벨 설정")
    print("=" * 60)
    environment_based_level()

    print("\n" + "=" * 60)
    print("4. 숫자 값")
    print("=" * 60)
    numeric_levels()
