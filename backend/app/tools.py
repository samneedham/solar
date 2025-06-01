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
    product_type: str  # e.g. "residential solar", "solar + battery", etc.

@function_tool(
    name_override="create_lead",
    description_override="Save a qualified lead to the CRM."
)
def create_lead(lead: LeadIn) -> str:
    """
    This function does not itself save to the database.
    Instead, when the agent calls create_lead(...),
    our backend intercepts and does the actual persistence.
    """
    return "lead_saved"