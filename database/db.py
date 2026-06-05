import sqlite3
from datetime import datetime
from pathlib import Path
import json

FILE_PATH = Path("/tmp/processed_orders.db")


def get_now():
    return datetime.utcnow().isoformat()

def get_connection():
    FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(FILE_PATH, check_same_thread=False)


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY,
                status TEXT,
                updated_at TEXT,
                payload TEXT,
                retry_count INTEGER DEFAULT 0
            )
        """)


def claim_order(order_id: str, payload: dict):
    now = get_now()

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR IGNORE INTO orders 
            (order_id, status, updated_at, payload, retry_count)
            VALUES (?, 'processing', ?, ?, 0)
        """, (order_id, now, json.dumps(payload)))

        return cursor.rowcount == 1


def claim_failed_order(order_id: str, max_retries: int = 5):
    now = get_now()

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE orders
            SET status = 'retrying',
                updated_at = ?
            WHERE order_id = ?
            AND status IN ('failed', 'retrying')
            AND retry_count < ?
        """, (now, order_id, max_retries))

        return cursor.rowcount == 1


def update_order_status(order_id: str, status: str):
    now = get_now()

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE orders
            SET status = ?,
                updated_at = ?
            WHERE order_id = ?
        """, (status, now, order_id))


def get_retryable_orders(max_retries: int = 5):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT order_id
            FROM orders
            WHERE status IN ('failed', 'retrying')
            AND retry_count < ?
        """, (max_retries,))

        return [row[0] for row in cursor.fetchall()]


def get_order_payload(order_id: str):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT payload
            FROM orders
            WHERE order_id = ?
        """, (order_id,))

        row = cursor.fetchone()

        if not row:
            return None

        return json.loads(row[0])


def get_retry_count(order_id: str):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT retry_count
            FROM orders
            WHERE order_id = ?
        """, (order_id,))

        row = cursor.fetchone()
        return row[0] if row else 0


def increment_retry_count(order_id: str):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE orders
            SET retry_count = retry_count + 1,
                updated_at = ?
            WHERE order_id = ?
        """, (get_now(), order_id))