# backend/app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./leads.db")
if _DATABASE_URL.startswith("postgres://"):
    _DATABASE_URL = _DATABASE_URL.replace("postgres://", "postgresql://", 1)

DATABASE_URL = _DATABASE_URL