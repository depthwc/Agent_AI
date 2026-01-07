from mcp.server.fastmcp import FastMCP
app = FastMCP()
@app.tool()
def greet(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    app.run(transport='stdio')