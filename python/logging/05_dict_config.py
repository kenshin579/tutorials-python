"""
logging.config.dictConfig - 딕셔너리 기반 설정
"""

import logging
import logging.config
import tempfile
import os


# ============================================================
# dictConfig 기반 설정
# ============================================================
def dict_config_example():
    """dictConfig()로 로깅 전체 구성하기"""
    log_dir = tempfile.mkdtemp()
    log_file = os.path.join(log_dir, "app.log")

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        # 포맷터 정의
        "formatters": {
            "simple": {
                "format": "%(levelname)-8s %(message)s",
            },
            "detailed": {
                "format": "%(asctime)s [%(name)s] %(levelname)-8s %(filename)s:%(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        # 핸들러 정의
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.FileHandler",
                "level": "WARNING",
                "formatter": "detailed",
                "filename": log_file,
                "encoding": "utf-8",
            },
            "rotating_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "detailed",
                "filename": os.path.join(log_dir, "rotating.log"),
                "maxBytes": 1048576,  # 1MB
                "backupCount": 5,
                "encoding": "utf-8",
            },
        },
        # 로거 정의
        "loggers": {
            "app": {
                "level": "DEBUG",
                "handlers": ["console", "file"],
                "propagate": False,
            },
            "app.database": {
                "level": "WARNING",
                "handlers": ["console", "rotating_file"],
                "propagate": False,
            },
        },
        # 루트 로거
        "root": {
            "level": "INFO",
            "handlers": ["console"],
        },
    }

    logging.config.dictConfig(config)

    # 로거 사용
    app_logger = logging.getLogger("app")
    db_logger = logging.getLogger("app.database")

    app_logger.debug("앱 디버그 메시지")
    app_logger.info("앱 시작")
    app_logger.warning("앱 경고 → 콘솔 + 파일")

    db_logger.info("DB 정보 → app.database 레벨(WARNING)에 의해 필터링됨")
    db_logger.warning("DB 경고 → 콘솔 + rotating 파일")

    print(f"\n로그 파일 내용 ({log_file}):")
    with open(log_file, encoding="utf-8") as f:
        content = f.read()
        print(content if content else "(비어 있음 - WARNING 이상만 기록)")


if __name__ == "__main__":
    dict_config_example()
