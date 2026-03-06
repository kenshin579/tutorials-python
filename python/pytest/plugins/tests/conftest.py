"""공유 fixture + 커스텀 hook 함수"""

import pytest

from src.calculator import Calculator


# === 공유 fixture ===


@pytest.fixture
def calculator():
    """Calculator 인스턴스를 제공하는 기본 fixture"""
    return Calculator()


@pytest.fixture
def user_factory():
    """factory fixture: 파라미터화된 객체 생성기"""

    def _create_user(name: str = "test", role: str = "admin"):
        return {"name": name, "role": role, "active": True}

    return _create_user


@pytest.fixture
def sample_data(tmp_path):
    """tmp_path를 활용한 임시 파일 fixture"""
    data_file = tmp_path / "sample.txt"
    data_file.write_text("hello\nworld\n")
    return data_file


# === 커스텀 hook 함수 ===


def pytest_configure(config):
    """설정 커스터마이징: 커스텀 마커 등록"""
    config.addinivalue_line("markers", "slow: 느린 테스트 (deselect with '-m \"not slow\"')")
    config.addinivalue_line("markers", "integration: 통합 테스트")


def pytest_collection_modifyitems(config, items):
    """테스트 수집 후 수정: slow 마커가 있는 테스트에 skip 조건 추가"""
    skip_slow = config.getoption("-m", default=None)
    if skip_slow == "not slow":
        skip_marker = pytest.mark.skip(reason="--m 'not slow' 옵션으로 제외")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_marker)


def pytest_runtest_makereport(item, call):
    """테스트 결과 후처리: 실패한 테스트 정보 출력"""
    if call.when == "call" and call.excinfo is not None:
        print(f"\n[FAILED] {item.nodeid}: {call.excinfo.typename}")
