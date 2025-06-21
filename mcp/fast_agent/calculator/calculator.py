#!/usr/bin/env python3
import asyncio
from mcp_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent("Calculator")


# 에이전트 함수 정의
@fast.agent(instruction="간단한 수식을 계산해줘")
async def main():
    # use the --model command line switch or agent arguments to change model
    async with fast.run() as agent:
        await agent.interactive()  # 대화형 모드 실행


if __name__ == "__main__":
    asyncio.run(main())
