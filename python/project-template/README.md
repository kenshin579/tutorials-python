# Python 프로젝트 템플릿

pyproject.toml 기반의 현대적 Python 프로젝트 구성 예제입니다.

## 기술 스택

- **패키지 매니저**: uv
- **린터/포매터**: ruff
- **타입 체커**: mypy
- **테스트**: pytest
- **환경변수**: python-dotenv
- **Git 훅**: pre-commit

## 시작하기

```bash
# 의존성 설치
uv sync

# 실행
uv run python -m myapp.main

# 테스트
uv run pytest

# 린트
uv run ruff check .

# 포맷 체크
uv run ruff format --check .

# 타입 체크
uv run mypy src/
```

## 프로젝트 구조

```
project-template/
├── pyproject.toml          # 프로젝트 설정 (PEP 621)
├── src/
│   └── myapp/
│       ├── __init__.py
│       ├── main.py         # 엔트리포인트
│       └── config.py       # 환경변수 로딩
├── tests/
│   └── test_main.py        # 테스트
├── .env.example            # 환경변수 템플릿
├── .pre-commit-config.yaml # pre-commit 훅
└── .github/workflows/
    └── ci.yml              # GitHub Actions CI
```
