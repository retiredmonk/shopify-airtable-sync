from fastapi import APIRouter, Request

from controller import handle_order_webhook
from middlewares.verify_shopify_webhook import verify_shopify_webhook

router = APIRouter()

@router.post(
    "/orders",
    summary="Shopify Order Creation webhook",
)

async def order_webhook_endpoint(request: Request):
    print("🔥 WEBHOOK HIT")

    try:
        await verify_shopify_webhook(request)
        print("✅ Verified")

        response = await handle_order_webhook(request)
        print("✅ Processed")

        return response

    except Exception as e:
        print("❌ ERROR:", str(e))
        raise