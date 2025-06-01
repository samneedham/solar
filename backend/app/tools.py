from agents import Tool
from pydantic import BaseModel, EmailStr, Field

class LeadIn(BaseModel):
    name: str | None
    email: EmailStr
    postcode: str = Field(..., pattern=r"[A-Z]{1,2}\d{1,2}[A-Z]?\s*\d[A-Z]{2}")
    product_type: str
    key_specs: dict = {}

create_lead = Tool(
    name="create_lead",
    description="Save a qualified lead to the CRM",
    parameters=LeadIn.model_json_schema(),
)