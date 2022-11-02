import uvicorn
from fastapi import FastAPI

from src.middlewares.header import ResponseHeaderMiddleware
from controllers import basic
from controllers import course

app = FastAPI()
app.add_middleware(ResponseHeaderMiddleware, version='1.0.4')
app.include_router(basic.router)
app.include_router(course.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8001,
        reload=True,
        debug=True,
        log_level="info",
    )
