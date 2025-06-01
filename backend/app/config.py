# backend/app/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # pick up .env at docker build/runtime

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Render (or some envs) may give "postgres://" but SQLAlchemy wants "postgresql://"
_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./leads.db")
if _DATABASE_URL.startswith("postgres://"):
    _DATABASE_URL = _DATABASE_URL.replace("postgres://", "postgresql://", 1)

DATABASE_URL = _DATABASE_URL