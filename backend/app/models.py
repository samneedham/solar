# models.py ---------------------------------------------------
from sqlmodel import SQLModel, Field

class Lead(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str | None
    email: str
    postcode: str
    product_type: str
    key_specs: dict | None = {}