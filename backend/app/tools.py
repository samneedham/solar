# backend/app/tools.py
from agents import function_tool
from pydantic import BaseModel, EmailStr, Field


class LeadIn(BaseModel):
    name: str | None
    email: EmailStr
    postcode: str = Field(
        ...,
        pattern=r"[A-Z]{1,2}\d{1,2}[A-Z]?\s*\d[A-Z]{2}",
        description="UK postcode",
    )
    product_type: str


@function_tool(
    name_override="create_lead",
    description_override="Save a qualified lead to the CRM."
)
def create_lead(lead: LeadIn) -> str:
    """
    This gets called by the agent when it has gathered everything it needs for a sales lead.
    The web-server (main.py) will intercept the call and store lead data in Postgres.
    """
    # We never write to the database here; main.py will handle persistence.
    return "lead_saved"