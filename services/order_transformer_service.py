def transform_order(payload: dict) -> dict:

    return {
        "Order ID": payload.get("id"),
        "Email": payload.get("email"),
        "Total Price": float(payload.get("total_price", 0)),
        "Currency": payload.get("currency"),
        "Created At": payload.get("created_at"),
        "Customer Name": (
            f"{payload.get('customer', {}).get('first_name', '')} "
            f"{payload.get('customer', {}).get('last_name', '')}"
        ).strip()
    }
