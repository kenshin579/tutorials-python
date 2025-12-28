#!/usr/bin/env python3
import asyncio

from mcp_agent.core.fastagent import FastAgent

fast = FastAgent("FileSystemAgent")

@fast.agent(
    instruction="List files",
    servers=["filesystem"]  # config.yaml의 이름
)
async def main():
    async with fast.run() as agent:
        await agent.interactive()

if __name__ == "__main__":
    asyncio.run(main())
