# backend/app/lead_agent.py
from agents import Agent, ModelSettings
from .tools import create_lead      # decorated with @function_tool

lead_agent = Agent(
    name="Lead-Collector",
    instructions=(
        "You are a friendly assistant matching homeowners with installers. "
        "Ask as few questions as possible to fill the create_lead tool."
    ),
    model="gpt-4o-mini",
    model_settings=ModelSettings(
        temperature=0.5,      # a bit of creativity
    ),
    tools=[create_lead],
)