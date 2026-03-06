"""Process 생성, Pool, Queue, Pipe, shared_memory"""

import unittest
import multiprocessing
import os


def square(n: int) -> int:
    return n * n


def add(a: int, b: int) -> int:
    return a + b


def worker_with_queue(q: multiprocessing.Queue, value: int):
    q.put(value * value)


def worker_with_pipe(conn, value: int):
    conn.send(value * value)
    conn.close()


def get_pid(q):
    q.put(os.getpid())


def update_shared(counter, arr):
    counter.value += 1
    for i in range(len(arr)):
        arr[i] = i * 1.5


class TestProcessBasic(unittest.TestCase):
    def test_process_create_and_join(self):
        """Process 생성과 join"""
        result = multiprocessing.Queue()
        p = multiprocessing.Process(target=get_pid, args=(result,))
        p.start()
        p.join()

        child_pid = result.get()
        # 자식 프로세스의 PID는 현재 프로세스와 다름
        assert child_pid != os.getpid()


class TestPool(unittest.TestCase):
    def test_pool_map(self):
        """Pool.map(): 여러 입력을 병렬로 처리"""
        with multiprocessing.Pool(2) as pool:
            results = pool.map(square, [1, 2, 3, 4, 5])
        assert results == [1, 4, 9, 16, 25]

    def test_pool_apply_async(self):
        """Pool.apply_async(): 비동기 작업 제출"""
        with multiprocessing.Pool(2) as pool:
            future1 = pool.apply_async(square, (10,))
            future2 = pool.apply_async(square, (20,))
            assert future1.get(timeout=5) == 100
            assert future2.get(timeout=5) == 400

    def test_pool_starmap(self):
        """Pool.starmap(): 여러 인자를 받는 함수 병렬 처리"""
        with multiprocessing.Pool(2) as pool:
            results = pool.starmap(add, [(1, 2), (3, 4), (5, 6)])
        assert results == [3, 7, 11]


class TestQueue(unittest.TestCase):
    def test_queue_communication(self):
        """Queue로 프로세스 간 통신"""
        q = multiprocessing.Queue()
        processes = []
        for i in range(3):
            p = multiprocessing.Process(target=worker_with_queue, args=(q, i))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        results = set()
        while not q.empty():
            results.add(q.get())

        assert results == {0, 1, 4}


class TestPipe(unittest.TestCase):
    def test_pipe_communication(self):
        """Pipe로 프로세스 간 1:1 통신"""
        parent_conn, child_conn = multiprocessing.Pipe()
        p = multiprocessing.Process(
            target=worker_with_pipe, args=(child_conn, 7)
        )
        p.start()
        result = parent_conn.recv()
        p.join()

        assert result == 49


class TestSharedMemory(unittest.TestCase):
    def test_shared_value_and_array(self):
        """Value와 Array로 프로세스 간 메모리 공유"""
        shared_counter = multiprocessing.Value("i", 0)
        shared_array = multiprocessing.Array("d", [0.0, 0.0, 0.0])

        p = multiprocessing.Process(
            target=update_shared, args=(shared_counter, shared_array)
        )
        p.start()
        p.join()

        assert shared_counter.value == 1
        assert list(shared_array) == [0.0, 1.5, 3.0]


if __name__ == "__main__":
    unittest.main()
