"""실전 CLI 팁 데모

실행 방법:
    pytest --lf tests/test_cli_tips.py       # 마지막 실패 테스트만 재실행
    pytest --sw tests/test_cli_tips.py       # stepwise: 실패 지점부터 재시작
    pytest --tb=short tests/test_cli_tips.py # traceback 형식 조절
    pytest --pdb tests/test_cli_tips.py      # 실패 시 디버거 진입
    pytest -p no:warnings tests/test_cli_tips.py  # 경고 숨기기
"""

import warnings

import pytest


# === --lf (last failed) 데모 ===


def test_always_passes():
    """항상 통과하는 테스트"""
    assert 1 + 1 == 2


def test_sometimes_fails():
    """조건에 따라 실패할 수 있는 테스트 (--lf 데모용)
    환경변수 FORCE_FAIL=1 설정 시 실패
    """
    import os

    if os.environ.get("FORCE_FAIL") == "1":
        pytest.fail("FORCE_FAIL 환경변수로 의도적 실패")
    assert True


# === --sw (stepwise) 데모 ===


def test_step_1():
    """Step 1: 데이터 준비"""
    data = [1, 2, 3]
    assert len(data) == 3


def test_step_2():
    """Step 2: 데이터 변환"""
    data = [x * 2 for x in [1, 2, 3]]
    assert data == [2, 4, 6]


def test_step_3():
    """Step 3: 결과 검증"""
    result = sum([2, 4, 6])
    assert result == 12


# === --tb (traceback) 데모 ===


def test_traceback_demo():
    """traceback 형식을 확인하기 위한 테스트
    --tb=short, --tb=long, --tb=line 으로 비교해보세요
    """
    expected = {"a": 1, "b": 2, "c": 3}
    actual = {"a": 1, "b": 2, "c": 3}
    assert actual == expected


# === -p no:warnings 데모 ===


def test_with_deprecation_warning():
    """DeprecationWarning을 발생시키는 테스트
    -p no:warnings 옵션으로 경고를 숨길 수 있다
    """
    with warnings.catch_warnings():
        warnings.simplefilter("always")
        warnings.warn("이 기능은 곧 제거됩니다", DeprecationWarning, stacklevel=1)
    assert True


# === 마커 활용 ===


@pytest.mark.slow
def test_slow_operation():
    """@pytest.mark.slow 마커가 적용된 테스트
    실행: pytest -m slow / pytest -m "not slow"
    """
    import time

    time.sleep(0.1)
    assert True
