"""커스텀 fixture 패턴 데모

- factory fixture: 파라미터화된 객체 생성기
- request fixture: 테스트 메타데이터 접근
- tmp_path / tmp_path_factory: 임시 파일/디렉토리
"""

import json

import pytest


# === factory fixture ===


class TestFactoryFixture:
    def test_default_user(self, user_factory):
        """기본값으로 사용자 생성"""
        user = user_factory()
        assert user["name"] == "test"
        assert user["role"] == "admin"
        assert user["active"] is True

    def test_custom_user(self, user_factory):
        """커스텀 파라미터로 사용자 생성"""
        user = user_factory(name="alice", role="viewer")
        assert user["name"] == "alice"
        assert user["role"] == "viewer"

    def test_multiple_users(self, user_factory):
        """여러 사용자를 한 번에 생성"""
        users = [user_factory(name=f"user_{i}") for i in range(3)]
        assert len(users) == 3
        assert users[0]["name"] == "user_0"


# === request fixture: 테스트 메타데이터 접근 ===


@pytest.fixture
def log_test_name(request):
    """request fixture로 현재 테스트 이름을 로깅"""
    test_name = request.node.name
    print(f"\n[START] {test_name}")
    yield test_name
    print(f"\n[END] {test_name}")


def test_with_request_fixture(log_test_name):
    """request fixture로 테스트 이름에 접근"""
    assert "test_with_request_fixture" in log_test_name


# === tmp_path: 임시 파일/디렉토리 ===


class TestTmpPath:
    def test_write_and_read(self, tmp_path):
        """tmp_path로 임시 파일 생성 후 읽기"""
        file = tmp_path / "output.txt"
        file.write_text("hello pytest")
        assert file.read_text() == "hello pytest"

    def test_json_file(self, tmp_path):
        """JSON 파일 읽기/쓰기"""
        data = {"name": "test", "values": [1, 2, 3]}
        json_file = tmp_path / "data.json"
        json_file.write_text(json.dumps(data))

        loaded = json.loads(json_file.read_text())
        assert loaded == data

    def test_nested_dirs(self, tmp_path):
        """중첩 디렉토리 생성"""
        nested = tmp_path / "a" / "b" / "c"
        nested.mkdir(parents=True)
        assert nested.exists()


# === tmp_path_factory: 세션 스코프 임시 디렉토리 ===


def test_tmp_path_factory(tmp_path_factory):
    """tmp_path_factory로 이름이 지정된 임시 디렉토리 생성"""
    base_dir = tmp_path_factory.mktemp("mydata")
    config_file = base_dir / "config.ini"
    config_file.write_text("[settings]\ndebug=true")
    assert config_file.exists()


# === conftest.py의 sample_data fixture 활용 ===


def test_sample_data(sample_data):
    """conftest.py에서 정의한 fixture 사용"""
    content = sample_data.read_text()
    lines = content.strip().split("\n")
    assert len(lines) == 2
    assert lines[0] == "hello"
