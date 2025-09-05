# db.py
import time
import pymysql
from typing import Optional, Sequence
from datetime import datetime
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

def _new_connection():
    return pymysql.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD,
        database=DB_NAME, charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor, autocommit=True,
    )

def connect_to_db(max_attempts: int = 10, delay_s: float = 2.0):
    attempts = 0
    while True:
        try: return _new_connection()
        except Exception:
            attempts += 1
            if attempts >= max_attempts: raise
            time.sleep(delay_s)

def fetchone(q: str, params: Optional[Sequence] = None):
    conn = connect_to_db()
    try:
        with conn.cursor() as cur:
            cur.execute(q, params or ())
            return cur.fetchone()
    finally:
        conn.close()

def fetchall(q: str, params: Optional[Sequence] = None):
    conn = connect_to_db()
    try:
        with conn.cursor() as cur:
            cur.execute(q, params or ())
            return cur.fetchall()
    finally:
        conn.close()

def execute(q: str, params: Optional[Sequence] = None):
    conn = connect_to_db()
    try:
        with conn.cursor() as cur:
            cur.execute(q, params or ())
            conn.commit()
    finally:
        conn.close()
