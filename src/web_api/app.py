from fastapi import FastAPI, Query
from starlette.responses import JSONResponse

app = FastAPI(title="Calculator Application")


@app.get(path="/add")
async def add(a: float = Query(description="First Parameter"),
              b: float = Query(description="Second Parameter")) -> JSONResponse:
    """Performs Addition Of 2 floating numbers - a and b and returns result"""
    value = a + b
    return JSONResponse(content=value, status_code=200)
