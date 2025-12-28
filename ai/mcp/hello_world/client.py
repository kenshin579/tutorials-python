import asyncio

import mcp
from fastmcp import Client

client = Client("server.py")

async def call_tool(name: str):
    async with client:
        result = await client.call_tool("greet", {"name": name})
        print(result)

asyncio.run(call_tool("Ford"))

# python client.py
# [05/30/25 18:14:45] INFO     Starting MCP server 'Hello World' with transport 'stdio'                                                                                                                                 server.py:799
# [TextContent(type='text', text='Hello, Ford!', annotations=None)]