"""하위 디렉토리 conftest 계층 구조 데모."""

from src.calculator import Calculator


class TestSubDirectory:
    """sub/ 디렉토리의 테스트."""

    def test_sub_only_fixture(self, sub_only_fixture):
        """sub/conftest.py에 정의된 fixture 사용 가능."""
        assert sub_only_fixture["scope"] == "sub"
        assert sub_only_fixture["value"] == 42

    def test_상위_conftest_fixture도_사용_가능(self, calculator):
        """상위 tests/conftest.py의 fixture도 접근 가능."""
        assert calculator.add(10, 20) == 30

    def test_두_fixture_동시_사용(self, calculator, sub_only_fixture):
        """상위 + 하위 conftest fixture를 동시에 사용."""
        result = calculator.multiply(sub_only_fixture["value"], 2)
        assert result == 84
