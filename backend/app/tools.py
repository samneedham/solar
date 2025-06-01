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
    key_specs: dict = {}

# The function body can be empty; we persist the lead server-side.
@function_tool(
    name_override="create_lead",
    description_override="Save a qualified lead to the CRM."
)
def create_lead(lead: LeadIn) -> str:        
    """
    This gets called by the agent; the web-server intercepts the call
    and stores lead data in Postgres.
    """
    return "lead_saved"