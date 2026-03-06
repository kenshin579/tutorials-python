"""DB 의존성 mocking - Repository 패턴 mock 주입."""

import pytest

from app.repository import User, UserRepository, UserServiceWithRepo


class TestRepositoryMocking:
    """Repository를 mock으로 교체하여 서비스 계층 테스트."""

    def test_mock_repository_기본(self, mocker, sample_user):
        """mocker.Mock(spec=)으로 Repository mock 생성."""
        mock_repo = mocker.Mock(spec=UserRepository)
        mock_repo.find_by_id.return_value = sample_user

        service = UserServiceWithRepo(mock_repo)
        result = service.get_user_display_name(1)

        assert result == "Frank Oh <frank@example.com>"
        mock_repo.find_by_id.assert_called_once_with(1)

    def test_사용자_없을_때_에러(self, mocker):
        """Repository가 None을 반환하면 ValueError 발생."""
        mock_repo = mocker.Mock(spec=UserRepository)
        mock_repo.find_by_id.return_value = None

        service = UserServiceWithRepo(mock_repo)

        with pytest.raises(ValueError, match="User 999 not found"):
            service.get_user_display_name(999)

    def test_전체_사용자_목록(self, mocker):
        """find_all() mock으로 목록 반환."""
        mock_repo = mocker.Mock(spec=UserRepository)
        mock_repo.find_all.return_value = [
            User(id=1, name="Frank", email="frank@test.com"),
            User(id=2, name="Alice", email="alice@test.com"),
        ]

        service = UserServiceWithRepo(mock_repo)
        names = service.get_all_user_names()

        assert names == ["Frank", "Alice"]
        mock_repo.find_all.assert_called_once()

    def test_사용자_생성(self, mocker):
        """save() mock으로 저장 동작 검증."""
        mock_repo = mocker.Mock(spec=UserRepository)
        mock_repo.save.return_value = User(id=10, name="Bob", email="bob@test.com")

        service = UserServiceWithRepo(mock_repo)
        user = service.create_user("Bob", "bob@test.com")

        assert user.id == 10
        assert user.name == "Bob"

        # save에 전달된 인자 확인
        saved_user = mock_repo.save.call_args.args[0]
        assert saved_user.name == "Bob"
        assert saved_user.email == "bob@test.com"


class TestFixtureBasedMocking:
    """fixture로 mock repository를 제공하는 패턴."""

    @pytest.fixture
    def mock_repo(self, mocker):
        """테스트용 mock repository fixture."""
        repo = mocker.Mock(spec=UserRepository)
        repo.find_by_id.return_value = User(id=1, name="Test User", email="test@test.com")
        repo.find_all.return_value = [
            User(id=1, name="Test User", email="test@test.com"),
        ]
        return repo

    @pytest.fixture
    def service(self, mock_repo):
        """mock_repo를 주입한 서비스 fixture."""
        return UserServiceWithRepo(mock_repo)

    def test_fixture_기반_테스트(self, service):
        """fixture로 의존성이 주입된 서비스 테스트."""
        result = service.get_user_display_name(1)
        assert result == "Test User <test@test.com>"

    def test_fixture_기반_목록_테스트(self, service):
        """fixture로 주입된 서비스에서 목록 조회."""
        names = service.get_all_user_names()
        assert names == ["Test User"]
