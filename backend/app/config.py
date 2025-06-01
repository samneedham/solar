import os
from dotenv import load_dotenv

load_dotenv()                      # .env in Docker build context
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL  = os.getenv("DATABASE_URL", "sqlite:///./leads.db")