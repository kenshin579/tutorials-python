"""pytest-xdist 데모: 병렬 테스트 실행

실행 방법:
    pytest -n auto tests/test_xdist.py          # CPU 코어 수만큼 워커 생성
    pytest -n 4 tests/test_xdist.py              # 워커 4개 지정
    pytest -n auto --dist=loadscope tests/test_xdist.py  # 모듈/클래스 단위 분배
"""

import os
import time


def test_worker_id_check(worker_id):
    """각 워커의 ID를 확인하여 병렬 실행을 검증한다.
    단일 실행: worker_id = "master"
    병렬 실행: worker_id = "gw0", "gw1", ...
    """
    print(f"Running on worker: {worker_id}")
    assert worker_id is not None


def test_parallel_task_1():
    """병렬 실행 확인용 태스크 1"""
    pid = os.getpid()
    print(f"Task 1 - PID: {pid}")
    time.sleep(0.1)
    assert True


def test_parallel_task_2():
    """병렬 실행 확인용 태스크 2"""
    pid = os.getpid()
    print(f"Task 2 - PID: {pid}")
    time.sleep(0.1)
    assert True


def test_parallel_task_3():
    """병렬 실행 확인용 태스크 3"""
    pid = os.getpid()
    print(f"Task 3 - PID: {pid}")
    time.sleep(0.1)
    assert True


class TestLoadScope:
    """--dist=loadscope 사용 시 같은 클래스의 테스트는 같은 워커에서 실행된다"""

    def test_scope_a(self, worker_id):
        print(f"LoadScope A - worker: {worker_id}")
        assert True

    def test_scope_b(self, worker_id):
        print(f"LoadScope B - worker: {worker_id}")
        assert True

    def test_scope_c(self, worker_id):
        print(f"LoadScope C - worker: {worker_id}")
        assert True
