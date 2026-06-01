import httpx
from config.shopifyConfig import get_shopify_config


config = get_shopify_config()

async def fetch_shopify_order(order_id: str):

    url = f"{config.BASE_URL}/admin/api/2023-10/orders/{order_id}.json"

    headers = {
        "X-Shopify-Access-Token": config.ACCESS_TOKEN,
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:

        response = await client.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception("Failed to fetch order from Shopify")

        return response.json()

