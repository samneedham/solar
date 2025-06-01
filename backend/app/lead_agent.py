# backend/app/lead_agent.py
from agents import Agent, ModelSettings
from .tools import create_lead  # the @function_tool

lead_agent = Agent(
    name="Lead-Collector",
    instructions=(
        "You are a friendly assistant for a free, impartial solar‐info service. "
        "Your main job is to give helpful solar/renewables details, but if a user wants a quote, you must collect exactly these four fields:\n"
        "  1. name (optional)\n"
        "  2. email (REQUIRED)\n"
        "  3. postcode (REQUIRED, UK format, e.g. SW1A 1AA)\n"
        "  4. product_type (REQUIRED; e.g. 'rooftop solar panels', 'battery storage')\n\n"
        "You may gather them in any order. If the user mentions any of these fields, store them. "
        "As soon as you have email, postcode, and product_type, immediately emit a single tool call:\n"
        "```json\n"
        "{\"name\": <value or null>, \"email\": <value>, \"postcode\": <value>, \"product_type\": <value>}\n"
        "```\n"
        "and STOP. Do not add any extra free‐text after the tool call. "
        "If any required field is missing, ask only for the missing pieces."
    ),
    model="gpt-4o-mini",
    model_settings=ModelSettings(
        temperature=0.5,
        tool_choice="required",
    ),
    tools=[create_lead],
    tool_use_behavior="stop_on_first_tool",
)