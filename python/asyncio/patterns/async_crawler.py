"""
실전 예제: 비동기 웹 크롤러
- Semaphore + Queue + httpx 조합
- 동시 요청 제한 + 생산자-소비자 패턴으로 URL을 크롤링한다
"""

import asyncio
import time

try:
    import httpx
except ImportError:
    httpx = None


# ============================================================
# 1. Semaphore + Queue 기반 비동기 크롤러
# ============================================================
class AsyncCrawler:
    """Semaphore + Queue를 활용한 비동기 웹 크롤러."""

    def __init__(self, max_concurrent: int = 5, num_workers: int = 3):
        self.sem = asyncio.Semaphore(max_concurrent)
        self.queue: asyncio.Queue[str] = asyncio.Queue()
        self.num_workers = num_workers
        self.results: dict[str, dict] = {}

    async def fetch(self, url: str) -> dict:
        """URL을 가져온다. Semaphore로 동시 요청을 제한한다."""
        async with self.sem:
            if httpx:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, timeout=10)
                    return {
                        "url": url,
                        "status": response.status_code,
                        "length": len(response.text),
                    }
            else:
                # httpx 없이 시뮬레이션
                await asyncio.sleep(0.1)
                return {
                    "url": url,
                    "status": 200,
                    "length": 1024,
                }

    async def worker(self, worker_id: int):
        """큐에서 URL을 꺼내 크롤링하는 워커."""
        while True:
            url = await self.queue.get()
            try:
                result = await self.fetch(url)
                self.results[url] = result
                print(f"  [Worker-{worker_id}] {url} -> {result['status']} ({result['length']} bytes)")
            except Exception as e:
                self.results[url] = {"url": url, "error": str(e)}
                print(f"  [Worker-{worker_id}] {url} -> 에러: {e}")
            finally:
                self.queue.task_done()

    async def crawl(self, urls: list[str]) -> dict[str, dict]:
        """URL 목록을 비동기로 크롤링한다."""
        # URL을 큐에 넣기
        for url in urls:
            await self.queue.put(url)

        # 워커 시작
        workers = [
            asyncio.create_task(self.worker(i))
            for i in range(self.num_workers)
        ]

        # 모든 작업 완료 대기
        await self.queue.join()

        # 워커 정리
        for w in workers:
            w.cancel()

        return self.results


async def crawler_example():
    """비동기 크롤러 실행 예제."""
    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/ip",
        "https://httpbin.org/user-agent",
        "https://httpbin.org/headers",
        "https://httpbin.org/delay/0",
    ]

    crawler = AsyncCrawler(max_concurrent=3, num_workers=3)

    start = time.monotonic()
    results = await crawler.crawl(urls)
    elapsed = time.monotonic() - start

    print(f"\n  크롤링 완료: {len(results)}개 URL, {elapsed:.2f}s 소요")
    return results


# ============================================================
# 2. 간단한 버전 - Semaphore만 사용
# ============================================================
async def simple_crawler(urls: list[str], max_concurrent: int = 5):
    """Semaphore만 사용하는 간단한 크롤러."""
    sem = asyncio.Semaphore(max_concurrent)
    results = {}

    async def fetch(url: str):
        async with sem:
            # 시뮬레이션
            await asyncio.sleep(0.1)
            result = {"url": url, "status": 200, "length": 512}
            results[url] = result
            print(f"  {url} -> {result['status']}")
            return result

    await asyncio.gather(*[fetch(url) for url in urls])
    return results


if __name__ == "__main__":
    print("=== 비동기 웹 크롤러 (Semaphore + Queue) ===")
    asyncio.run(crawler_example())

    print("\n=== 간단한 크롤러 (Semaphore만) ===")
    urls = [f"https://example.com/page/{i}" for i in range(10)]
    asyncio.run(simple_crawler(urls, max_concurrent=3))
