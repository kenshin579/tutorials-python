# server.py
from fastmcp import FastMCP, Client

# Create an MCP server
mcp = FastMCP("Hello World")

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


@mcp.tool()
def greet(name: str) -> str:
    return f"Hello, {name}!"

client = Client(mcp)

async def call_tool(name: str):
    async with client:
        result = await client.call_tool("greet", {"name": name})
        print(result)

if __name__ == "__main__":
    mcp.run()

# run differently
# fastmcp run server.py:mcp