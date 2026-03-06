"""fixture: scope, yield, autouse, 의존성 주입."""

import pytest

from src.calculator import Calculator


class TestFixtureBasic:
    """@pytest.fixture 기본 사용법."""

    def test_conftest_fixture_사용(self, calculator):
        """conftest.py에 정의된 calculator fixture를 인자로 받는다."""
        assert calculator.add(2, 3) == 5

    def test_sample_data_fixture(self, sample_data):
        """conftest.py에 정의된 sample_data fixture 사용."""
        assert sum(sample_data["numbers"]) == sample_data["expected_sum"]


class TestFixtureScope:
    """fixture scope 종류: function, class, module, session."""

    call_count = 0

    @pytest.fixture(scope="function")
    def function_scope_fixture(self):
        """각 테스트 함수마다 새로 생성 (기본값)."""
        TestFixtureScope.call_count += 1
        return TestFixtureScope.call_count

    def test_function_scope_1(self, function_scope_fixture):
        """매번 새 인스턴스."""
        assert isinstance(function_scope_fixture, int)

    def test_function_scope_2(self, function_scope_fixture):
        """이전 테스트와 다른 인스턴스."""
        assert isinstance(function_scope_fixture, int)


# module scope fixture는 모듈 레벨에서 정의
@pytest.fixture(scope="module")
def module_calculator():
    """모듈 전체에서 하나의 인스턴스를 공유."""
    print("\n[module_calculator] 생성됨")
    return Calculator()


class TestModuleScope:
    def test_module_scope_1(self, module_calculator):
        assert module_calculator.add(1, 1) == 2

    def test_module_scope_2(self, module_calculator):
        """같은 인스턴스를 재사용한다."""
        assert module_calculator.multiply(3, 4) == 12


class TestYieldFixture:
    """yield fixture: setup + teardown 패턴."""

    @pytest.fixture
    def resource(self):
        """yield 앞: setup, yield 뒤: teardown."""
        print("\n[setup] 리소스 초기화")
        data = {"connection": "open", "items": []}
        yield data
        print("\n[teardown] 리소스 정리")
        data["connection"] = "closed"
        data["items"].clear()

    def test_yield_fixture(self, resource):
        """yield로 반환된 값을 사용."""
        assert resource["connection"] == "open"
        resource["items"].append("item1")
        assert len(resource["items"]) == 1


class TestAutouse:
    """autouse=True: 자동 적용 fixture."""

    log = []

    @pytest.fixture(autouse=True)
    def log_test_name(self, request):
        """각 테스트 시작 시 자동으로 실행 (인자로 받을 필요 없음)."""
        TestAutouse.log.append(request.node.name)
        yield
        # teardown

    def test_autouse_1(self):
        assert "test_autouse_1" in TestAutouse.log

    def test_autouse_2(self):
        assert "test_autouse_2" in TestAutouse.log


class TestFixtureDependency:
    """fixture 간 의존성 주입 (fixture가 fixture를 인자로 받기)."""

    @pytest.fixture
    def base_number(self):
        return 10

    @pytest.fixture
    def doubled_number(self, base_number):
        """base_number fixture에 의존."""
        return base_number * 2

    @pytest.fixture
    def calc_result(self, calculator, base_number):
        """conftest의 calculator와 base_number에 동시 의존."""
        return calculator.add(base_number, 5)

    def test_fixture_chain(self, doubled_number):
        assert doubled_number == 20

    def test_multi_dependency(self, calc_result):
        assert calc_result == 15
