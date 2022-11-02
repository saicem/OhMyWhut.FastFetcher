import uvicorn
from fastapi import FastAPI

from controllers import basic
from controllers import course
from src.middlewares.header import ResponseHeaderMiddleware

app = FastAPI()
app.add_middleware(ResponseHeaderMiddleware, version='1.1.1')
app.include_router(basic.router)
app.include_router(course.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
        debug=True,
        log_level="info",
    )
