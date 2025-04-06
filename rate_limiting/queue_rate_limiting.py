import random
import threading
import time
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import requests


class RateLimiter:
    def __init__(self, max_calls, per_seconds):
        self.max_calls = max_calls
        self.per_seconds = per_seconds
        self.lock = threading.Lock()
        self.call_timestamps = deque()

    def acquire(self):
        with self.lock:
            now = time.time()
            while self.call_timestamps and self.call_timestamps[0] <= now - self.per_seconds:
                self.call_timestamps.popleft()

            if len(self.call_timestamps) >= self.max_calls:
                wait_time = self.per_seconds - (now - self.call_timestamps[0])
                if wait_time > 0:
                    time.sleep(wait_time)

            self.call_timestamps.append(time.time())


class StockFetcher:
    def __init__(self, rate_limiter):
        self.rate_limiter = rate_limiter

    def fetch_stock_current_price(self, stock_code):
        self.rate_limiter.acquire()

        url = "http://httpbin.org/get"
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{start_time}:{stock_code}: calling stock price")

        response = requests.get(url)
        data = response.json()

        wait_time = random.uniform(1, 2)
        time.sleep(wait_time)

        print(f"{start_time}:{stock_code} Stock price fetched")
        return data


def main():
    rate_limiter = RateLimiter(max_calls=20, per_seconds=1)
    fetcher = StockFetcher(rate_limiter)

    stock_codes = [f"STOCK{i}" for i in range(50)]

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetcher.fetch_stock_current_price, code) for code in stock_codes]

        # Wait for all threads to complete
        for future in futures:
            result = future.result()


if __name__ == "__main__":
    main()
