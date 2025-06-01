# backend/app/lead_agent.py
from agents import Agent, ModelSettings
from .tools import create_lead

lead_agent = Agent(
    name="Lead-Collector",
    instructions=(
        "You are a friendly assistant for a free, impartial solar‐info service. "
        "Your main job is to give helpful solar/renewables details. "
        "If a user wants a quote, collect exactly these four fields:\n"
        "  1. name (optional)\n"
        "  2. email (REQUIRED)\n"
        "  3. postcode (REQUIRED, UK format, e.g. SW1A 1AA)\n"
        "  4. product_type (REQUIRED; e.g. 'rooftop solar panels', 'battery storage')\n\n"
        "You may gather them in any order. As soon as you have email, postcode, and product_type, "
        "emit a single tool call in JSON form and STOP. Do not output any extra text after that call. "
        "If a required field is missing, ask only for the missing fields."
    ),
    model="gpt-4o-mini",
    model_settings=ModelSettings(
        temperature=0.5,
        tool_choice="required",  # force use of create_lead once fields are complete
    ),
    tools=[create_lead],
    tool_use_behavior="stop_on_first_tool",
)