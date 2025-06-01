import os
from dotenv import load_dotenv

load_dotenv()  # load .env from your build context

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./leads.db"  # fallback if not set
)

# If Render (or some other host) gave you a "postgres://" URL,
# SQLAlchemy expects "postgresql://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)