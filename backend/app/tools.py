# backend/app/tools.py
from agents import function_tool
from pydantic import BaseModel, EmailStr, Field

class LeadIn(BaseModel):
    name: str | None
    email: EmailStr
    postcode: str = Field(
        ...,
        pattern=r"[A-Z]{1,2}\d{1,2}[A-Z]?\s*\d[A-Z]{2}",
        description="UK postcode (e.g. SW1A 1AA)",
    )
    product_type: str

@function_tool(
    name_override="create_lead",
    description_override="Save a qualified lead to the CRM."
)
def create_lead(lead: LeadIn) -> str:
    """
    This will be intercepted by main.py; the function body can stay empty.
    """
    return "lead_saved"