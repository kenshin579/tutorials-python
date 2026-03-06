"""
asyncio.Queue 생산자-소비자 패턴
- asyncio.Queue(maxsize=N): 비동기 큐 생성
- put/get, join/task_done
- 다중 생산자-다중 소비자 구조
- PriorityQueue, LifoQueue 변형
"""

import asyncio
import random
import time


# ============================================================
# 1. 기본 Queue 사용법
# ============================================================
async def basic_queue():
    """기본적인 asyncio.Queue put/get 사용법."""
    queue: asyncio.Queue[str] = asyncio.Queue(maxsize=5)

    # 데이터 넣기
    for i in range(5):
        await queue.put(f"item-{i}")
    print(f"  큐 크기: {queue.qsize()}")

    # 데이터 꺼내기
    results = []
    while not queue.empty():
        item = await queue.get()
        results.append(item)
        queue.task_done()

    print(f"  꺼낸 데이터: {results}")
    return results


# ============================================================
# 2. 단일 생산자-단일 소비자
# ============================================================
async def single_producer_consumer():
    """단일 생산자와 단일 소비자 패턴."""
    queue: asyncio.Queue[int] = asyncio.Queue(maxsize=3)
    processed = []

    async def producer():
        for i in range(10):
            await queue.put(i)
            print(f"  [생산] item={i}, 큐 크기={queue.qsize()}")
            await asyncio.sleep(0.05)
        # 종료 신호
        await queue.put(None)

    async def consumer():
        while True:
            item = await queue.get()
            if item is None:
                queue.task_done()
                break
            await asyncio.sleep(0.1)  # 처리 시간 시뮬레이션
            processed.append(item)
            queue.task_done()
            print(f"  [소비] item={item}")

    await asyncio.gather(producer(), consumer())
    print(f"  처리 완료: {processed}")
    return processed


# ============================================================
# 3. 다중 생산자-다중 소비자
# ============================================================
async def multi_producer_consumer():
    """다중 생산자-다중 소비자 패턴."""
    queue: asyncio.Queue[tuple[str, int]] = asyncio.Queue(maxsize=10)
    processed = []

    async def producer(name: str, count: int):
        for i in range(count):
            item = (name, i)
            await queue.put(item)
            await asyncio.sleep(random.uniform(0.01, 0.05))
        print(f"  [생산자 {name}] {count}개 생산 완료")

    async def consumer(name: str):
        while True:
            try:
                item = await asyncio.wait_for(queue.get(), timeout=0.5)
            except asyncio.TimeoutError:
                print(f"  [소비자 {name}] 타임아웃 - 종료")
                break
            await asyncio.sleep(random.uniform(0.01, 0.05))
            processed.append(item)
            queue.task_done()

    # 2명의 생산자, 3명의 소비자
    producers = [producer("P1", 5), producer("P2", 5)]
    consumers = [consumer("C1"), consumer("C2"), consumer("C3")]

    await asyncio.gather(*producers, *consumers)
    print(f"  총 처리 건수: {len(processed)}")
    return processed


# ============================================================
# 4. queue.join()으로 모든 작업 완료 대기
# ============================================================
async def queue_join_example():
    """queue.join()으로 모든 작업이 완료될 때까지 대기한다."""
    queue: asyncio.Queue[int] = asyncio.Queue()
    results = []

    async def worker(name: str):
        while True:
            item = await queue.get()
            await asyncio.sleep(0.05)
            results.append(item)
            print(f"  [{name}] 처리 완료: {item}")
            queue.task_done()

    # 워커 3개 생성
    workers = [asyncio.create_task(worker(f"W{i}")) for i in range(3)]

    # 작업 투입
    for i in range(9):
        await queue.put(i)

    # 모든 작업 완료 대기
    await queue.join()
    print(f"  모든 작업 완료! 결과: {sorted(results)}")

    # 워커 정리
    for w in workers:
        w.cancel()

    return sorted(results)


# ============================================================
# 5. PriorityQueue - 우선순위 큐
# ============================================================
async def priority_queue_example():
    """PriorityQueue는 우선순위(낮은 값)가 높은 항목을 먼저 반환한다."""
    queue: asyncio.PriorityQueue[tuple[int, str]] = asyncio.PriorityQueue()

    # (우선순위, 데이터) 형태로 삽입
    await queue.put((3, "낮은 우선순위"))
    await queue.put((1, "높은 우선순위"))
    await queue.put((2, "중간 우선순위"))

    results = []
    while not queue.empty():
        priority, data = await queue.get()
        results.append((priority, data))
        print(f"  우선순위 {priority}: {data}")
        queue.task_done()

    return results


# ============================================================
# 6. LifoQueue - 스택 (후입선출)
# ============================================================
async def lifo_queue_example():
    """LifoQueue는 마지막에 넣은 항목을 먼저 반환한다."""
    queue: asyncio.LifoQueue[str] = asyncio.LifoQueue()

    for item in ["first", "second", "third"]:
        await queue.put(item)

    results = []
    while not queue.empty():
        item = await queue.get()
        results.append(item)
        print(f"  꺼낸 항목: {item}")
        queue.task_done()

    return results


if __name__ == "__main__":
    print("=== 1. 기본 Queue ===")
    asyncio.run(basic_queue())

    print("\n=== 2. 단일 생산자-소비자 ===")
    asyncio.run(single_producer_consumer())

    print("\n=== 3. 다중 생산자-소비자 ===")
    asyncio.run(multi_producer_consumer())

    print("\n=== 4. queue.join() ===")
    asyncio.run(queue_join_example())

    print("\n=== 5. PriorityQueue ===")
    asyncio.run(priority_queue_example())

    print("\n=== 6. LifoQueue ===")
    asyncio.run(lifo_queue_example())
