"""프로젝트 전역 fixture 정의."""

import pytest

from src.calculator import Calculator


@pytest.fixture
def calculator():
    """Calculator 인스턴스를 제공하는 fixture."""
    return Calculator()


@pytest.fixture
def sample_data():
    """공통 테스트 데이터."""
    return {
        "numbers": [1, 2, 3, 4, 5],
        "expected_sum": 15,
    }
