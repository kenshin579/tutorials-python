import asyncio
import random
import time
from datetime import datetime
from unittest import TestCase

import aiohttp
from aiolimiter import AsyncLimiter


class AiolimiterTest(TestCase):
    @classmethod
    def setUpClass(cls):
        max_concurrent = 5
        cls.limiter = AsyncLimiter(max_concurrent, time_period=1)  # 20 calls per second

    def test_run_concurrently(self):
        stock_list = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA"] * 4 * 5
        # stock_list = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA"]
        start_time = time.time()

        stock_data = asyncio.run(self.fetch_stocks(stock_list))
        elapsed_time = time.time() - start_time

        print(f"elapsed_time: {elapsed_time}, size: {len(stock_list)}, stock_data: {stock_data}")

    async def fetch_stock_current_price(self, stock_code):
        async with self.limiter:
            url = "http://httpbin.org/get"

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"{start_time}:{stock_code}: calling stock price")

                    data = await response.json()

                    wait_time = random.uniform(1, 2)  # 1~2초 랜덤 딜레이

                    await asyncio.sleep(wait_time)
                    print(f"{start_time}:{stock_code} Stock price fetched")
                    return data

    async def fetch_stocks(self, stock_list):
        # create a list of tasks
        tasks = [self.fetch_stock_current_price(code) for code in stock_list]

        # run the tasks concurrently
        results = await asyncio.gather(*tasks)

        for result in results:
            print(result)
