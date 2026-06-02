from fastapi import HTTPException

def validate_payload(payload: dict):

    if not payload:
        raise HTTPException(status_code=400, detail="Empty payload")

    required_fields = ["id", "name", "total_price"]

    for field in required_fields:
        if field not in payload or payload[field] is None:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")

    try:
        float(payload.get("total_price",0))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid price")


    return True
