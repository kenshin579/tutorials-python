from typing import Annotated

from fastapi import Depends, Query


# --- 함수 기반 의존성: yield 패턴 (DB 세션 시뮬레이션) ---
def get_db():
    """DB 세션을 시뮬레이션하는 yield 의존성."""
    db = {"connection": "active"}
    print("DB 세션 열림")
    try:
        yield db
    finally:
        print("DB 세션 닫힘")


# --- 클래스 기반 의존성: 공통 쿼리 파라미터 ---
class CommonQueryParams:
    """여러 엔드포인트에서 공유하는 공통 쿼리 파라미터."""

    def __init__(
        self,
        skip: int = Query(default=0, ge=0, description="건너뛸 항목 수"),
        limit: int = Query(default=10, ge=1, le=100, description="반환할 최대 항목 수"),
    ):
        self.skip = skip
        self.limit = limit


# --- 의존성 체이닝: 인증 시뮬레이션 ---
def get_current_user(db=Depends(get_db)):
    """DB 의존성에 의존하는 인증 의존성 (체이닝)."""
    return {"user_id": 1, "username": "admin", "db_status": db["connection"]}


# 타입 별칭
CommonParams = Annotated[CommonQueryParams, Depends()]
DB = Annotated[dict, Depends(get_db)]
CurrentUser = Annotated[dict, Depends(get_current_user)]
