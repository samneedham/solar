# backend/app/models.py
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON


class Lead(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = None
    email: str
    postcode: str
    product_type: str

    # If the agent gathers additional specs (e.g. solar panel tilt, roof pitch, etc.),
    # stash them in this JSON column.
    key_specs: dict | None = Field(
        default_factory=dict,
        sa_column=Column(JSON)
    )