"""
핸들러 종류 - StreamHandler, FileHandler, RotatingFileHandler, TimedRotatingFileHandler
"""

import logging
import os
import tempfile
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler


# ============================================================
# 1. StreamHandler - 콘솔 출력
# ============================================================
def stream_handler_example():
    """StreamHandler로 콘솔 출력"""
    import sys

    logger = logging.getLogger("stream_demo")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    # stdout으로 출력
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(
        logging.Formatter("[STDOUT] %(levelname)s - %(message)s")
    )

    # stderr로 출력 (기본값)
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)
    stderr_handler.setFormatter(
        logging.Formatter("[STDERR] %(levelname)s - %(message)s")
    )

    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)

    logger.info("stdout으로 출력됩니다")
    logger.error("stdout과 stderr 모두에 출력됩니다")


# ============================================================
# 2. FileHandler - 파일 출력
# ============================================================
def file_handler_example():
    """FileHandler로 파일에 로그 기록"""
    log_dir = tempfile.mkdtemp()
    log_file = os.path.join(log_dir, "app.log")

    logger = logging.getLogger("file_demo")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(file_handler)

    logger.info("파일에 기록되는 로그입니다")
    logger.warning("한글도 잘 기록됩니다")

    # 파일 내용 확인
    with open(log_file, encoding="utf-8") as f:
        print(f"로그 파일 ({log_file}):")
        print(f.read())


# ============================================================
# 3. RotatingFileHandler - 파일 크기 기반 로테이션
# ============================================================
def rotating_file_handler_example():
    """RotatingFileHandler로 파일 크기 제한"""
    log_dir = tempfile.mkdtemp()
    log_file = os.path.join(log_dir, "rotating.log")

    logger = logging.getLogger("rotating_demo")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    # maxBytes: 파일 최대 크기 (500 바이트)
    # backupCount: 백업 파일 수 (3개)
    handler = RotatingFileHandler(
        log_file,
        maxBytes=500,
        backupCount=3,
        encoding="utf-8",
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(handler)

    # 로그를 많이 남겨서 로테이션 발생시키기
    for i in range(50):
        logger.info(f"로테이션 테스트 메시지 #{i:03d}")

    # 생성된 파일 확인
    print(f"로그 디렉토리: {log_dir}")
    for f in sorted(os.listdir(log_dir)):
        filepath = os.path.join(log_dir, f)
        size = os.path.getsize(filepath)
        print(f"  {f} ({size} bytes)")


# ============================================================
# 4. TimedRotatingFileHandler - 시간 기반 로테이션
# ============================================================
def timed_rotating_handler_example():
    """TimedRotatingFileHandler로 시간 기반 로테이션"""
    log_dir = tempfile.mkdtemp()
    log_file = os.path.join(log_dir, "timed.log")

    logger = logging.getLogger("timed_demo")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    # when: 로테이션 주기
    #   'S' = 초, 'M' = 분, 'H' = 시간
    #   'D' = 일, 'midnight' = 자정
    #   'W0'-'W6' = 요일 (월-일)
    handler = TimedRotatingFileHandler(
        log_file,
        when="S",  # 초 단위 (데모용)
        interval=1,
        backupCount=5,
        encoding="utf-8",
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(handler)

    logger.info("시간 기반 로테이션 로그")
    print(f"로그 파일: {log_file}")
    print("프로덕션에서는 when='midnight'를 주로 사용합니다")


# ============================================================
# 5. 복수 핸들러 - 콘솔 + 파일 동시 출력
# ============================================================
def multiple_handlers_example():
    """콘솔과 파일에 동시에 로그 출력 (서로 다른 레벨)"""
    log_dir = tempfile.mkdtemp()
    log_file = os.path.join(log_dir, "multi.log")

    logger = logging.getLogger("multi_demo")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    # 콘솔: DEBUG 이상 모두 출력
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(
        logging.Formatter("[콘솔] %(levelname)-8s %(message)s")
    )

    # 파일: WARNING 이상만 기록
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    )

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.debug("디버그 → 콘솔에만 출력")
    logger.info("정보 → 콘솔에만 출력")
    logger.warning("경고 → 콘솔 + 파일")
    logger.error("에러 → 콘솔 + 파일")

    print(f"\n파일에 기록된 내용 ({log_file}):")
    with open(log_file, encoding="utf-8") as f:
        print(f.read())


if __name__ == "__main__":
    print("=" * 60)
    print("1. StreamHandler - 콘솔 출력")
    print("=" * 60)
    stream_handler_example()

    print("\n" + "=" * 60)
    print("2. FileHandler - 파일 출력")
    print("=" * 60)
    file_handler_example()

    print("\n" + "=" * 60)
    print("3. RotatingFileHandler - 크기 기반 로테이션")
    print("=" * 60)
    rotating_file_handler_example()

    print("\n" + "=" * 60)
    print("4. TimedRotatingFileHandler - 시간 기반 로테이션")
    print("=" * 60)
    timed_rotating_handler_example()

    print("\n" + "=" * 60)
    print("5. 복수 핸들러 - 콘솔 + 파일")
    print("=" * 60)
    multiple_handlers_example()
