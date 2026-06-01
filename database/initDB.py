import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import json

FILE_PATH = Path("Data/processed_orders.db")


def get_connection():
    return sqlite3.connect(FILE_PATH, check_same_thread=False)


def init_db():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            status TEXT,
            updated_at TEXT,
            payload TEXT,
            retry_count INTEGER DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()


def claim_order(order_id: str, payload: dict):
    connection = get_connection()
    cursor = connection.cursor()

    now = datetime.utcnow().isoformat()

    cursor.execute("""
        INSERT OR IGNORE INTO orders 
        (order_id, status, updated_at, payload, retry_count)
        VALUES (?, 'processing', ?, ?, 0)
    """, (order_id, now, json.dumps(payload)))

    connection.commit()
    inserted = cursor.rowcount == 1

    connection.close()
    return inserted


def claim_failed_order(order_id: str):
    connection = get_connection()
    cursor = connection.cursor()

    now = datetime.utcnow().isoformat()

    cursor.execute("""
        UPDATE orders
        SET status = 'retrying', updated_at = ?
        WHERE order_id = ?
        AND status IN ('failed', 'retrying')
    """, (now, order_id))

    connection.commit()
    claimed = cursor.rowcount == 1

    connection.close()
    return claimed


def update_order_status(order_id: str, status: str):
    connection = get_connection()
    cursor = connection.cursor()

    now = datetime.utcnow().isoformat()

    cursor.execute("""
        UPDATE orders
        SET status = ?, updated_at = ?
        WHERE order_id = ?
    """, (status, now, order_id))

    connection.commit()
    connection.close()

def get_retryable_orders():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT order_id
        FROM orders
        WHERE status IN ('failed', 'retrying')
        AND status != 'permanent_failed'
    """)

    results = [row[0] for row in cursor.fetchall()]
    connection.close()
    return results


def get_order_payload(order_id: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT payload FROM orders WHERE order_id = ?
    """, (order_id,))

    row = cursor.fetchone()
    connection.close()

    if not row:
        return None

    return json.loads(row[0])


def get_retry_count(order_id: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT retry_count FROM orders WHERE order_id = ?
    """, (order_id,))

    row = cursor.fetchone()
    connection.close()

    return row[0] if row else 0


def increment_retry_count(order_id: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE orders
        SET retry_count = retry_count + 1
        WHERE order_id = ?
    """, (order_id,))

    connection.commit()
    connection.close()