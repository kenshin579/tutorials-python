"""Thread 생성/join, Lock, Event, daemon thread"""

import unittest
import threading
import time


class TestThreadBasic(unittest.TestCase):
    def test_thread_create_and_join(self):
        """Thread 생성, start, join 기본 패턴"""
        results = []

        def worker(name: str):
            time.sleep(0.05)
            results.append(name)

        t1 = threading.Thread(target=worker, args=("thread-1",))
        t2 = threading.Thread(target=worker, args=("thread-2",))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        assert len(results) == 2
        assert set(results) == {"thread-1", "thread-2"}

    def test_thread_with_return_value(self):
        """Thread에서 결과 반환: 공유 리스트 사용"""
        results = {}

        def worker(name: str, n: int):
            results[name] = sum(range(n))

        t1 = threading.Thread(target=worker, args=("a", 100))
        t2 = threading.Thread(target=worker, args=("b", 200))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        assert results["a"] == 4950
        assert results["b"] == 19900


class TestLock(unittest.TestCase):
    def test_race_condition_without_lock(self):
        """Lock 없이 공유 변수 접근: race condition 가능"""
        counter = {"value": 0}

        def increment():
            for _ in range(100_000):
                counter["value"] += 1

        threads = [threading.Thread(target=increment) for _ in range(2)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # race condition으로 200000보다 작을 수 있음
        # (항상 재현되지는 않으므로 단순히 실행만 확인)
        assert counter["value"] <= 200_000

    def test_lock_prevents_race_condition(self):
        """Lock으로 race condition 방지"""
        counter = {"value": 0}
        lock = threading.Lock()

        def increment():
            for _ in range(100_000):
                with lock:
                    counter["value"] += 1

        threads = [threading.Thread(target=increment) for _ in range(2)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert counter["value"] == 200_000


class TestEvent(unittest.TestCase):
    def test_event_signaling(self):
        """Event로 스레드 간 신호 전달"""
        event = threading.Event()
        result = {"received": False}

        def waiter():
            event.wait(timeout=1.0)
            result["received"] = True

        def sender():
            time.sleep(0.05)
            event.set()

        t1 = threading.Thread(target=waiter)
        t2 = threading.Thread(target=sender)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        assert result["received"] is True
        assert event.is_set()


class TestDaemonThread(unittest.TestCase):
    def test_daemon_thread(self):
        """daemon thread: 메인 스레드 종료 시 함께 종료"""
        result = {"ran": False}

        def background_task():
            result["ran"] = True

        t = threading.Thread(target=background_task, daemon=True)
        assert t.daemon is True
        t.start()
        t.join(timeout=1.0)

        assert result["ran"] is True

    def test_non_daemon_thread(self):
        """non-daemon thread (기본값): 메인 스레드가 대기"""
        t = threading.Thread(target=lambda: None)
        assert t.daemon is False


if __name__ == "__main__":
    unittest.main()
