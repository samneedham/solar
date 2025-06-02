import os
from dotenv import load_dotenv

load_dotenv()  # load .env from build context

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./leads.db"  # fallback if not set
)

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)