from agents import Agent
from .tools import create_lead


lead_agent = Agent(
    name="Lead-Collector",
    instructions=(
        "You are a friendly assistant matching homeowners with installers. "
        "Ask as few questions as possible to fill the create_lead tool."
    ),
    tools=[create_lead],
    model_config={"model": "gpt-4o-mini"},   # ultra-fast public landing page
)