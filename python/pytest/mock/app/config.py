import os


def get_api_url() -> str:
    """환경변수에서 API URL을 읽어 반환."""
    return os.environ.get("API_URL", "https://api.example.com")


def get_debug_mode() -> bool:
    """환경변수에서 디버그 모드 확인."""
    return os.environ.get("DEBUG", "false").lower() == "true"


def get_database_url() -> str:
    """환경변수에서 DB URL을 읽어 반환."""
    url = os.environ.get("DATABASE_URL")
    if url is None:
        raise RuntimeError("DATABASE_URL 환경변수가 설정되지 않았습니다")
    return url
