"""
FastAPI 로깅 - 미들웨어 기반 요청/응답 로그
"""

import logging
import time
import uuid

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

# 로거 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s - %(message)s",
    force=True,
)
logger = logging.getLogger("fastapi_app")


# ============================================================
# 요청/응답 로깅 미들웨어
# ============================================================
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """HTTP 요청/응답을 자동으로 로깅하는 미들웨어"""

    async def dispatch(self, request: Request, call_next):
        # 요청 ID 생성
        request_id = str(uuid.uuid4())[:8]
        start_time = time.time()

        # 요청 로그
        logger.info(
            "[%s] %s %s (client: %s)",
            request_id,
            request.method,
            request.url.path,
            request.client.host if request.client else "unknown",
        )

        # 요청 처리
        response = await call_next(request)

        # 응답 로그
        duration_ms = (time.time() - start_time) * 1000
        logger.info(
            "[%s] %s %s → %d (%.1fms)",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )

        # 응답 헤더에 요청 ID 추가
        response.headers["X-Request-ID"] = request_id
        return response


app.add_middleware(RequestLoggingMiddleware)


# ============================================================
# API 엔드포인트
# ============================================================
@app.get("/")
async def root():
    logger.debug("홈 엔드포인트 호출")
    return {"message": "Hello, World!"}


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    logger.info("사용자 조회: user_id=%d", user_id)
    return {"user_id": user_id, "name": f"User {user_id}"}


@app.get("/error")
async def trigger_error():
    logger.error("의도적 에러 발생")
    raise ValueError("테스트 에러")


if __name__ == "__main__":
    import uvicorn

    print("FastAPI 서버 시작: http://localhost:8000")
    print("API 문서: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
