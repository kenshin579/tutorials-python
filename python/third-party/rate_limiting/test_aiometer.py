import asyncio
import functools
import random
import time
from datetime import datetime
from unittest import TestCase
import aiohttp
import aiometer
import logging
from collections import defaultdict


class AiometerTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.max_at_once = 10  # 주어진 시간에 동시에 실행되는 작업의 최대 수를 제한하는 데 사용
        cls.max_per_second = 20  # 초당 생성되는 작업 수를 제한

        # 로깅 설정
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
        cls.logger = logging.getLogger(__name__)

        # 시간별 호출 횟수를 기록할 딕셔너리
        cls.calls_per_second = defaultdict(int)

    def test_run_concurrently(self):
        stock_list = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA"] * 4 * 5
        start_time = time.time()

        asyncio.run(self.fetch_stocks(stock_list))
        elapsed_time = time.time() - start_time

        # 호출 통계 분석
        self.analyze_call_rate()

        print(f"elapsed_time: {elapsed_time}, size: {len(stock_list)}")

    async def fetch_stock_current_price(self, stock_code):
        url = "http://httpbin.org/get"

        # 현재 초를 키로 호출 횟수 증가
        current_second = int(time.time())
        self.__class__.calls_per_second[current_second] += 1

        async with aiohttp.ClientSession() as session:
            start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            self.logger.info(f"호출 시작: {stock_code} - {start_time}")

            async with session.get(url) as response:
                data = await response.json()

                wait_time = random.uniform(1, 2)  # 1~2초 랜덤 딜레이
                await asyncio.sleep(wait_time)

                end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                self.logger.info(f"호출 완료: {stock_code} - {end_time}")
                return data

    async def fetch_stocks(self, stock_list):
        # create a list of tasks
        tasks = [functools.partial(self.fetch_stock_current_price, code) for code in stock_list]

        # run the tasks concurrently
        results = await aiometer.run_all(
            tasks,
            max_per_second=self.max_per_second,
            max_at_once=self.max_at_once
        )

        return results

    def analyze_call_rate(self):
        """호출 비율 분석 및 결과 출력"""
        if not self.__class__.calls_per_second:
            print("호출 데이터가 없습니다.")
            return

        print("\n===== 초당 API 호출 횟수 분석 =====")
        max_calls = max(self.__class__.calls_per_second.values())

        for second, count in sorted(self.__class__.calls_per_second.items()):
            timestamp = datetime.fromtimestamp(second).strftime('%H:%M:%S')
            print(f"시간: {timestamp}, 호출 수: {count}")

        print(f"\n최대 초당 호출 횟수: {max_calls}")
        print(f"설정된 max_per_second: {self.max_per_second}")
        print(f"제한 준수 여부: {'준수' if max_calls <= self.max_per_second else '초과'}")
        print("================================\n")