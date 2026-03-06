"""
YAML 파일에서 logging 설정 로드하기
"""

import logging
import logging.config
import os

import yaml


def yaml_config_example():
    """YAML 파일로 로깅 설정 로드"""
    config_path = os.path.join(os.path.dirname(__file__), "logging_config.yaml")

    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    logging.config.dictConfig(config)

    # 로거 사용
    app_logger = logging.getLogger("app")
    api_logger = logging.getLogger("app.api")

    app_logger.debug("YAML 설정으로 로드된 앱 로거 (DEBUG)")
    app_logger.info("앱 정보 메시지")

    api_logger.info("API 정보 메시지")
    api_logger.warning("API 경고 메시지")


if __name__ == "__main__":
    yaml_config_example()
