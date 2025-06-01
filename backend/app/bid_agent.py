# backend/app/bid_agent.py
from agents import Agent, ModelSettings
from .tools import price_sheet

bid_agent = Agent(
    name="Bid-Assistant",
    instructions="Given a lead JSON, return a total installed price in GBP.",
    model="gpt-4o-mini",
    model_settings=ModelSettings(
        temperature=0,        # deterministic
        # tool_choice="auto",  # default, omit if fine
    ),
    tools=[price_sheet],
)