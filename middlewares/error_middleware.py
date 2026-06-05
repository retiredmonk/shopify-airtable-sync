from fastapi.responses import JSONResponse
from utils.logger import logger


async def global_exception_handler(exc: Exception):

    logger.error(f"Unhandled error: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Something went wrong"
        }
    )