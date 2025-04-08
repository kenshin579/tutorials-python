import random
import threading
import time
from collections import deque, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import logging
import requests


class RateLimiter:
    def __init__(self, max_calls, per_seconds):
        self.max_calls = max_calls
        self.per_seconds = per_seconds
        self.lock = threading.Lock()
        self.call_timestamps = deque()

        # 호출 통계 추적을 위한 딕셔너리
        self.calls_per_second = defaultdict(int)

    def acquire(self):
        with self.lock:
            now = time.time()

            # 만료된 타임스탬프 제거
            while self.call_timestamps and self.call_timestamps[0] <= now - self.per_seconds:
                self.call_timestamps.popleft()

            # 호출 제한에 도달했다면 대기
            if len(self.call_timestamps) >= self.max_calls:
                wait_time = self.per_seconds - (now - self.call_timestamps[0])
                if wait_time > 0:
                    time.sleep(wait_time)
                    now = time.time()  # 대기 후 시간 업데이트

            # 호출 기록
            current_second = int(now)
            self.calls_per_second[current_second] += 1
            self.call_timestamps.append(now)

    def get_stats(self):
        """호출 통계 분석 결과 반환"""
        stats = {
            "calls_per_second": dict(self.calls_per_second),
            "max_calls_in_one_second": max(self.calls_per_second.values()) if self.calls_per_second else 0,
            "total_calls": sum(self.calls_per_second.values()),
            "seconds_tracked": len(self.calls_per_second)
        }
        return stats

    def print_stats(self):
        """호출 통계 출력"""
        if not self.calls_per_second:
            print("호출 데이터가 없습니다.")
            return

        print("\n===== 초당 API 호출 횟수 분석 =====")
        max_calls = max(self.calls_per_second.values())

        for second, count in sorted(self.calls_per_second.items()):
            timestamp = datetime.fromtimestamp(second).strftime('%H:%M:%S')
            print(f"시간: {timestamp}, 호출 수: {count}")

        print(f"\n최대 초당 호출 횟수: {max_calls}")
        print(f"설정된 max_calls: {self.max_calls}")
        print(f"제한 준수 여부: {'준수' if max_calls <= self.max_calls else '초과'}")
        print(f"총 호출 횟수: {sum(self.calls_per_second.values())}")
        print("================================\n")


class StockFetcher:
    def __init__(self, rate_limiter):
        self.rate_limiter = rate_limiter
        # 로깅 설정
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def fetch_stock_current_price(self, stock_code):
        self.rate_limiter.acquire()

        url = "http://httpbin.org/get"
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        self.logger.info(f"호출 시작: {stock_code} - {start_time}")


        response = requests.get(url)
        data = response.json()

        wait_time = random.uniform(1, 2)
        time.sleep(wait_time)

        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        self.logger.info(f"호출 완료: {stock_code} - {end_time}")
        return data


def main():
    rate_limiter = RateLimiter(max_calls=20, per_seconds=1)
    fetcher = StockFetcher(rate_limiter)

    # 테스트 용으로 더 많은 요청 생성 (50개 -> 100개)
    stock_codes = [f"STOCK{i}" for i in range(100)]
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=20) as executor:  # 스레드 수 증가
        futures = [executor.submit(fetcher.fetch_stock_current_price, code) for code in stock_codes]

        # 모든 스레드가 완료될 때까지 대기
        for future in futures:
            result = future.result()
            print(result)

    elapsed_time = time.time() - start_time
    print(f"총 실행 시간: {elapsed_time:.2f}초, 요청 수: {len(stock_codes)}")

    # 통계 출력
    rate_limiter.print_stats()


if __name__ == "__main__":
    main()