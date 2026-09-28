"""비동기 API 호출 서비스 - pytest-asyncio 데모용"""

import aiohttp


class AsyncService:
    def __init__(self, base_url: str = "https://httpbin.org"):
        self.base_url = base_url
        self._session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def fetch_json(self, path: str) -> dict:
        session = await self._get_session()
        async with session.get(f"{self.base_url}{path}") as response:
            response.raise_for_status()
            return await response.json()

    async def post_json(self, path: str, data: dict) -> dict:
        session = await self._get_session()
        async with session.post(f"{self.base_url}{path}", json=data) as response:
            response.raise_for_status()
            return await response.json()

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()
