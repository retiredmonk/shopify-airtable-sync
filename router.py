from fastapi import APIRouter, Request
from controller import handle_order_webhook
from middlewares.verify_shopify_webhook import verify_shopify_webhook

router = APIRouter()

@router.post(
    "/orders",
    summary="Shopify Order Creation webhook",
)

async def order_webhook_endpoint(request: Request):
    await verify_shopify_webhook(request)

    return await handle_order_webhook(request)