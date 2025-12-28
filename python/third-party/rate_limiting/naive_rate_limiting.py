import concurrent.futures
import random
import time
from datetime import datetime
from functools import wraps
from unittest import TestCase

import requests


class SimpleRateLimitingTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.max_concurrent = 5  # 동시에 실행할 최대 요청 수
        cls.max_per_second = 20
        cls.last_called_time = 0
        cls.interval = 1.0 / cls.max_per_second  # 각 호출 사이의 최소 간격

    def rate_limited(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()
            elapsed = current_time - self.__class__.last_called_time

            # 마지막 호출 이후 시간이 interval보다 작으면 대기
            if elapsed < self.__class__.interval:
                time.sleep(self.__class__.interval - elapsed)

            # 마지막 호출 시간 업데이트
            self.__class__.last_called_time = time.time()

            # 원본 함수 호출
            return func(*args, **kwargs)

        return wrapper

    def test_run_concurrently(self):
        stock_list = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA"] * 4 * 5
        start_time = time.time()

        # 래퍼 함수를 사용하여 fetch_stock_current_price 호출
        rate_limited_fetch = self.rate_limited(self.fetch_stock_current_price)

        # ThreadPoolExecutor를 사용하여 동시에 20개의 요청 실행
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_concurrent) as executor:
            # 작업 제출하고 결과 수집
            futures = [executor.submit(rate_limited_fetch, stock) for stock in stock_list]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]

        elapsed_time = time.time() - start_time
        print(f"elapsed_time: {elapsed_time}, size: {len(stock_list)}")
        return results

    def fetch_stock_current_price(self, stock_code):
        url = "http://httpbin.org/get"

        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{start_time}:{stock_code}: calling stock price")

        # call api
        resp = requests.get(url)
        data = resp.json()

        wait_time = random.uniform(1, 2)  # 1~2초 랜덤 딜레이

        time.sleep(wait_time)
        print(f"{start_time}:{stock_code} Stock price fetched")
        return data