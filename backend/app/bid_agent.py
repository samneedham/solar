from agents import Agent
from .tools import price_sheet        # define your own CSV lookup tool

bid_agent = Agent(
    name="Bid-Assistant",
    instructions="Given a lead JSON, return a total installed price in GBP.",
    tools=[price_sheet],
    model_config={"model": "gpt-4o"},
)