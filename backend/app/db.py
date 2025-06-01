# backend/app/db.py
from sqlmodel import create_engine, Session
from .config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False, connect_args={})

def get_session():
    with Session(engine) as session:
        yield session