import asyncio
from fastapi import FastAPI
import uvicorn

from router import router
from middlewares.requestLogger import log_requests
from middlewares.errorMiddleware import global_exception_handler
from services.retryService import retry_worker_loop
from database.initDB import init_db

app = FastAPI(
    title="Shopify Order Webhook Storage Service",
    version="1.0.0",
)

app.middleware("http")(log_requests)
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(
    router,
    prefix="/webhook",
    tags=["Shopify Order Webhook Storage Service"],
)


@app.on_event("startup")
async def startup():
    init_db()
    async def safe_worker_loop():
        try:
            await retry_worker_loop()
        except Exception as e:
            print("Retry Worker Crashed:", str(e))

    asyncio.create_task(safe_worker_loop())


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)