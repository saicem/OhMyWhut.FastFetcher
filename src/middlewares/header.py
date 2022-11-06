from urllib.request import Request

from starlette.middleware.base import BaseHTTPMiddleware


class ResponseHeaderMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        version,
    ):
        super().__init__(app)
        self.version = version

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers.append("x-app-version", self.version)
        return response
