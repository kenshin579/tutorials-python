"""
포맷터 커스터마이징 - 포맷 속성, datefmt, colorlog
"""

import logging


# ============================================================
# 1. 주요 포맷 속성
# ============================================================
def format_attributes_example():
    """포맷터에서 사용할 수 있는 주요 속성들"""
    logger = logging.getLogger("format_demo")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    # 다양한 포맷 속성 조합
    formats = {
        "기본": "%(levelname)s - %(message)s",
        "시간 포함": "%(asctime)s - %(levelname)s - %(message)s",
        "모듈 정보": "%(asctime)s [%(name)s] %(levelname)s - %(message)s",
        "호출 위치": "%(asctime)s %(filename)s:%(lineno)d (%(funcName)s) - %(message)s",
        "프로세스/스레드": "%(asctime)s [PID:%(process)d TID:%(thread)d] %(message)s",
    }

    for name, fmt in formats.items():
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(fmt))
        logger.handlers = [handler]
        print(f"\n--- {name} ---")
        logger.info("포맷 테스트 메시지")


# ============================================================
# 2. datefmt - 시간 형식 커스터마이징
# ============================================================
def datefmt_example():
    """시간 형식(datefmt) 커스터마이징"""
    logger = logging.getLogger("datefmt_demo")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    date_formats = {
        "기본 (None)": None,
        "ISO 형식": "%Y-%m-%dT%H:%M:%S",
        "한국 형식": "%Y년 %m월 %d일 %H시%M분%S초",
        "간결한 형식": "%H:%M:%S",
    }

    for name, datefmt in date_formats.items():
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(message)s", datefmt=datefmt)
        )
        logger.handlers = [handler]
        print(f"\n--- {name} ---")
        logger.info("시간 형식 테스트")


# ============================================================
# 3. colorlog - 컬러 출력
# ============================================================
def colorlog_example():
    """colorlog 라이브러리로 컬러 로그 출력"""
    try:
        import colorlog

        logger = logging.getLogger("color_demo")
        logger.setLevel(logging.DEBUG)
        logger.handlers.clear()

        handler = logging.StreamHandler()
        handler.setFormatter(
            colorlog.ColoredFormatter(
                "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(name)s%(reset)s - %(message)s",
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "red,bg_white",
                },
            )
        )
        logger.addHandler(handler)

        logger.debug("디버그 메시지 (cyan)")
        logger.info("정보 메시지 (green)")
        logger.warning("경고 메시지 (yellow)")
        logger.error("에러 메시지 (red)")
        logger.critical("치명적 에러 메시지 (red, bg_white)")

    except ImportError:
        print("colorlog가 설치되지 않았습니다: pip install colorlog")


if __name__ == "__main__":
    print("=" * 60)
    print("1. 포맷 속성")
    print("=" * 60)
    format_attributes_example()

    print("\n" + "=" * 60)
    print("2. 시간 형식 (datefmt)")
    print("=" * 60)
    datefmt_example()

    print("\n" + "=" * 60)
    print("3. colorlog 컬러 출력")
    print("=" * 60)
    colorlog_example()
