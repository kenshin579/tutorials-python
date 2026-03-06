"""
loguru 기본 사용법 - 간편한 로깅
"""

import os
import tempfile

from loguru import logger


# ============================================================
# 1. 즉시 사용 - 설정 없이 바로 로깅
# ============================================================
def instant_usage():
    """loguru는 import만 하면 즉시 사용 가능"""
    logger.debug("디버그 메시지")
    logger.info("정보 메시지")
    logger.warning("경고 메시지")
    logger.error("에러 메시지")
    logger.critical("치명적 에러 메시지")

    # 구조화된 데이터 로깅
    logger.info("사용자 로그인 성공: user_id={uid}, ip={ip}", uid=123, ip="192.168.1.1")


# ============================================================
# 2. 파일 핸들러 추가
# ============================================================
def file_handler_example():
    """logger.add()로 파일 핸들러 추가"""
    log_dir = tempfile.mkdtemp()

    # 기본 파일 핸들러
    log_file = os.path.join(log_dir, "app.log")
    logger.add(log_file, encoding="utf-8")
    logger.info("파일에 기록되는 로그")

    # 크기 기반 로테이션
    rotating_file = os.path.join(log_dir, "rotating.log")
    logger.add(
        rotating_file,
        rotation="10 MB",      # 10MB마다 로테이션
        retention="7 days",    # 7일 보관
        compression="zip",     # 오래된 파일 압축
        encoding="utf-8",
    )
    logger.info("로테이션 설정된 파일 로그")

    # 시간 기반 로테이션
    timed_file = os.path.join(log_dir, "daily.log")
    logger.add(
        timed_file,
        rotation="00:00",      # 매일 자정 로테이션
        retention=10,          # 최대 10개 파일 보관
        encoding="utf-8",
    )
    logger.info("일별 로테이션 파일 로그")

    print(f"로그 디렉토리: {log_dir}")
    for f in sorted(os.listdir(log_dir)):
        print(f"  {f}")


# ============================================================
# 3. 레벨 필터링
# ============================================================
def level_filtering():
    """레벨별 필터링"""
    log_dir = tempfile.mkdtemp()

    # WARNING 이상만 파일에 기록
    error_file = os.path.join(log_dir, "errors.log")
    logger.add(error_file, level="WARNING", encoding="utf-8")

    # 특정 모듈만 필터링
    logger.add(
        os.path.join(log_dir, "filtered.log"),
        filter=lambda record: "database" in record["message"],
        encoding="utf-8",
    )

    logger.debug("디버그 → errors.log에는 기록 안 됨")
    logger.warning("경고 → errors.log에 기록됨")
    logger.info("database 연결 성공 → filtered.log에 기록됨")


# ============================================================
# 4. 포맷 커스터마이징
# ============================================================
def format_customization():
    """로그 포맷 커스터마이징"""
    # 기본 핸들러 제거 후 커스텀 포맷 적용
    logger.remove()  # 모든 핸들러 제거

    # 커스텀 포맷
    logger.add(
        lambda msg: print(msg, end=""),
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
               "<level>{message}</level>",
        colorize=True,
    )

    logger.info("커스텀 포맷 로그")
    logger.warning("컬러와 포맷이 적용됩니다")

    # 기본 핸들러 복원
    logger.remove()
    logger.add(lambda msg: print(msg, end=""), colorize=True)


if __name__ == "__main__":
    print("=" * 60)
    print("1. 즉시 사용")
    print("=" * 60)
    instant_usage()

    print("\n" + "=" * 60)
    print("2. 파일 핸들러")
    print("=" * 60)
    file_handler_example()

    print("\n" + "=" * 60)
    print("3. 레벨 필터링")
    print("=" * 60)
    level_filtering()

    print("\n" + "=" * 60)
    print("4. 포맷 커스터마이징")
    print("=" * 60)
    format_customization()
