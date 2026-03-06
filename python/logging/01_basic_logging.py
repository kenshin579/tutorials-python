"""
logging 모듈 기본 - Logger, Handler, Formatter
"""

import logging

# ============================================================
# 1. basicConfig - 가장 간단한 설정
# ============================================================
def basic_config_example():
    """basicConfig()로 빠르게 설정하기"""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("basicConfig로 설정한 로거입니다")
    logger.debug("디버그 메시지도 출력됩니다")


# ============================================================
# 2. 수동 설정 - Handler와 Formatter를 직접 구성
# ============================================================
def manual_config_example():
    """핸들러와 포맷터를 직접 구성하기"""
    logger = logging.getLogger("manual_logger")
    logger.setLevel(logging.DEBUG)

    # 기존 핸들러 제거 (중복 방지)
    logger.handlers.clear()

    # 콘솔 핸들러 생성
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # 포맷터 설정
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)

    # 핸들러를 로거에 추가
    logger.addHandler(console_handler)

    logger.info("수동 설정 로거입니다")
    logger.debug("핸들러와 포맷터를 직접 구성했습니다")


# ============================================================
# 3. 로거 계층 구조 - 점(.) 표기법
# ============================================================
def logger_hierarchy_example():
    """로거 계층 구조와 전파(propagation)"""
    # 로거 계층: root -> app -> app.services -> app.services.user
    root_logger = logging.getLogger()
    app_logger = logging.getLogger("app")
    service_logger = logging.getLogger("app.services")
    user_logger = logging.getLogger("app.services.user")

    # root 로거에만 핸들러 설정
    root_logger.setLevel(logging.DEBUG)
    root_logger.handlers.clear()
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("[%(name)s] %(levelname)s - %(message)s")
    )
    root_logger.addHandler(handler)

    # 하위 로거에서 로그를 남기면 상위로 전파됨
    print("=== propagate=True (기본값) ===")
    user_logger.info("사용자 서비스 로그 - 상위 로거로 전파됩니다")
    service_logger.warning("서비스 계층 로그")
    app_logger.error("앱 계층 로그")

    # propagate=False로 설정하면 상위로 전파하지 않음
    print("\n=== propagate=False ===")
    service_logger.propagate = False
    service_logger.handlers.clear()
    service_handler = logging.StreamHandler()
    service_handler.setFormatter(
        logging.Formatter("[SERVICE ONLY] %(name)s - %(message)s")
    )
    service_logger.addHandler(service_handler)
    service_logger.warning("이 로그는 상위로 전파되지 않습니다")

    # 정리
    service_logger.propagate = True


# ============================================================
# 4. getLogger(__name__) 패턴
# ============================================================
def module_logger_example():
    """__name__을 사용한 모듈별 로거 생성 패턴"""
    # __name__은 현재 모듈의 이름 (예: '__main__' 또는 'package.module')
    logger = logging.getLogger(__name__)
    logger.info(f"현재 모듈 이름: {__name__}")
    logger.info("모듈별 로거를 사용하면 로그 출처를 쉽게 파악할 수 있습니다")


if __name__ == "__main__":
    print("=" * 60)
    print("1. basicConfig 예제")
    print("=" * 60)
    basic_config_example()

    print("\n" + "=" * 60)
    print("2. 수동 설정 예제")
    print("=" * 60)
    manual_config_example()

    print("\n" + "=" * 60)
    print("3. 로거 계층 구조 예제")
    print("=" * 60)
    logger_hierarchy_example()

    print("\n" + "=" * 60)
    print("4. 모듈별 로거 예제")
    print("=" * 60)
    module_logger_example()
