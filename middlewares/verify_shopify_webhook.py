import hmac
import hashlib
import base64
from fastapi import Request, HTTPException
from env import get_settings

config = get_settings()

async def verify_shopify_webhook(request: Request):

    body = request.state.body
    received_hmac = request.headers.get("X-Shopify-Hmac-Sha256")

    if not received_hmac:
        raise HTTPException(status_code=401, detail="Missing HMAC Header")

    computed_hmac = base64.b64encode(
        hmac.new(
            config.SHOPIFY_WEBHOOK_SECRET.encode("utf-8"),
            body,
            hashlib.sha256
        ).digest()
    ).decode()

    if not hmac.compare_digest(received_hmac, computed_hmac):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")
