"""하위 디렉토리 전용 conftest.py (계층별 적용 범위 데모)."""

import pytest


@pytest.fixture
def sub_only_fixture():
    """이 fixture는 tests/sub/ 하위에서만 사용 가능하다."""
    return {"scope": "sub", "value": 42}
