from fastmcp import FastMCP

mcp = FastMCP("Simple Calculator")


@mcp.tool()
def perform_addition(a: float, b: float) -> float:
    """ Performs Addition Of 2 Numbers - a and b and returns result"""
    print(f'MCP Tool - perform_addition in use')
    return a + b


@mcp.tool()
def perform_multiplication(a: float, b: float) -> float:
    """ Performs multiplication Of 2 floating numbers - a and b and returns result"""
    print(f'MCP Tool - perform_addition in use')
    return round(a * b, 2)


if __name__ == "__main__":
    mcp.run()
