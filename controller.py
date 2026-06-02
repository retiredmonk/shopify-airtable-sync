import json
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from services.order_processing_service import process_order
from utils.logger import logger
from utils.validator import _validate_payload


async def handle_order_webhook(request: Request):

    if not hasattr(request.state, "body"):
        raise HTTPException(status_code=400, detail="Request body missing")

    try:
        payload = json.loads(request.state.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise HTTPException(status_code=400, detail="Invalid JSON payload")


    _validate_payload(payload)

    logger.info(f"Received Shopify Order with ID:{payload['id']} Webhook")

    result = await process_order(payload)

    if result.get("status") == "duplicate":
        return JSONResponse(
            status_code=200,
            content={
                "status": "ignored",
                "message": "Duplicate order skipped"
            }
        )

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Order processed successfully",
            "data": result.get("data")
        }
    )