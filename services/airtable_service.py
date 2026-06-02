import httpx
import asyncio
from config.airtable_config import get_airtable_config
from utils.logger import logger

config = get_airtable_config()

async def send_to_airtable(data: dict):

    url =  f"https://api.airtable.com/v0/{config.BASE_ID}/{config.TABLE_NAME}"

    headers = {
        "Authorization": f"Bearer {config.API_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "records":[{
            "fields": data
        }]
    }

    max_retries = 3

    async with httpx.AsyncClient(timeout=10.0) as client:
        for attempt in range(1, max_retries+1):
            try:
                response = await client.post(url, json=payload, headers=headers)

                if response.status_code in (200, 201):
                    logger.info(f"Order with ID:{data.get('Order ID')} is successfully sent to Airtable")
                    return response.json()

                logger.error(f"Failed sending order with ID:{data.get('Order ID')} due to an Airtable API Error: {response.text}")

                if attempt == max_retries:
                    raise Exception(f"failed to send after max retries")

            except (httpx.RequestError, httpx.TimeoutException) as e:
                logger.error(f"Network error (attempt {attempt}): {str(e)}")

                if attempt == max_retries:
                    raise Exception(f"Failure while sending data to Airtable")

            await asyncio.sleep(2)
        return None

