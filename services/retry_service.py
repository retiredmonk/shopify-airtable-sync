import asyncio
from database.db import (
    get_retryable_orders,
    claim_failed_order,
    update_order_status,
    get_order_payload,
    get_retry_count,
    increment_retry_count,
    get_connection
)
from services.order_transformer_service import transform_order
from services.airtable_service import send_to_airtable
from utils.logger import logger

lock = asyncio.Lock()
connection = get_connection()

MAX_RETRIES = 5


async def retry_failed_orders():

    orders = get_retryable_orders(connection)

    for order_id in orders:

        claimed = claim_failed_order(connection, order_id)

        if not claimed:
            continue

        try:
            payload = get_order_payload(order_id)

            if not payload:
                logger.error(f"No payload found for {order_id}")
                continue

            retry_count = get_retry_count(order_id)

            if retry_count >= MAX_RETRIES:
                logger.error(f"Order {order_id} exceeded retry limit")
                update_order_status(order_id, "permanent_failed")
                continue

            logger.info(f"Retrying order {order_id} (attempt {retry_count + 1})")

            transformed_data = transform_order(payload)
            await send_to_airtable(transformed_data)

            update_order_status(order_id, "completed")
            logger.info(f"Retry successful for {order_id}")

        except Exception as e:
            logger.error(f"Retry failed for {order_id}: {str(e)}")

            increment_retry_count(order_id)
            update_order_status(order_id, "failed")

async def retry_worker_loop():
    while True:
        async with lock:
            await retry_failed_orders()
        await asyncio.sleep(60)