# config.py
import os
from dotenv import load_dotenv

load_dotenv()

def load_token() -> str:
    raw = os.environ["DISCORD_TOKEN"]
    tok = raw.strip().strip('"').strip("'")
    if tok.count(".") != 2:
        raise RuntimeError("DISCORD_TOKEN invalide: Bot Token attendu.")
    return tok

DISCORD_TOKEN = load_token()

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "greentown")
DB_USER = os.getenv("DB_USER", "botuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "botpass")
