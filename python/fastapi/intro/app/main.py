from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import users

app = FastAPI(
    title="FastAPI 입문 예제",
    description="FastAPI의 기본 구조, 라우팅, 의존성 주입, 자동 문서화 예제",
    version="0.1.0",
)

# CORS 미들웨어
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 프로덕션에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)


@app.get("/", tags=["root"])
def root():
    return {"message": "FastAPI 입문 예제 API"}


@app.get("/health", tags=["root"])
async def health_check():
    """async def 엔드포인트 예시."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
