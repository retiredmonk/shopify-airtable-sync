from fastapi import Request
from utils.logger import logger

async def log_requests(request: Request, call_next):

    body = await request.body()
    request.state.body = body

    logger.info({
        "method": request.method,
        "url": str(request.url),
        "body_preview": body[:200].decode("utf-8", errors="ignore"),
    })
    response = await call_next(request)
    return response