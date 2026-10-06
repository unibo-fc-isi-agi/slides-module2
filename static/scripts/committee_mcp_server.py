# pip install mcp
from mcp.server.fastmcp import FastMCP
from committee import tools

server = FastMCP("committee", instructions="Tools to inspect the applications to a PhD programme")
for function in tools:
    server.tool()(function)  # name, description, and input schema are derived from the function

if __name__ == "__main__":
    server.run()  # over stdio, by default; use server.run("streamable-http") to serve over HTTP
