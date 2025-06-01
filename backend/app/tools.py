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

# The function body can be empty; we persist the lead server-