# backend/app/lead_agent.py
from agents import Agent
from .tools import create_lead          # ← now the decorated function

lead_agent = Agent(
    name="Lead-Collector",
    instructions=(
        "You are a friendly assistant matching homeowners with installers. "
        "Ask as few questions as possible to fill the create_lead tool."
    ),
    tools=[create_lead],                # list of function_tools
    model_config={"model": "gpt-4o-mini"},
)