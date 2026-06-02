from database.db import claim_order, update_order_status
from services.order_transformer_service import _transform_order
from services.airtable_service import _send_to_airtable
from utils.logger import logger

async def process_order(payload: dict):

    order_id = str(payload["id"])

    claimed = claim_order(order_id, payload)

    if not claimed:
        logger.info(f"Duplicate order skipped: {order_id}")
        return {"status": "duplicate"}

    try:
        transformed_data = _transform_order(payload)
        logger.info(f"Order {order_id} transformed")

        airtable_response = await _send_to_airtable(transformed_data)
        logger.info(f"Order {order_id} sent to Airtable")

        update_order_status(order_id, "completed")

        return {"status": "processed", "data": airtable_response}

    except Exception as e:
        logger.error(f"Order {order_id} failed: {str(e)}")
        update_order_status(order_id, "failed")
        raise