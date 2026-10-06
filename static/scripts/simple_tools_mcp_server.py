# pip install mcp
from mcp.server.fastmcp import FastMCP
from simple_tools import tools

server = FastMCP("simple-tools", instructions="Tools to get the current time, the weather, and Web search results")
for function in tools:
    server.tool()(function)  # name, description, and input schema are derived from the function

if __name__ == "__main__":
    server.run()  # over stdio, by default; use server.run("streamable-http") to serve over HTTP
