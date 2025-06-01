# backend/app/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # load .env if present

# Read our OpenAI key (if you need it elsewhere) and the DATABASE_URL from env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Render often gives a DATABASE_URL that starts with "postgres://"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./leads.db")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)