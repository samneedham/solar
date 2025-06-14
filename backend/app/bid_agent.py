from agents import Agent, ModelSettings
from .tools import price_sheet  # assuming have a price_sheet tool elsewhere (actually OpenSolar)

bid_agent = Agent(
    name="Bid-Assistant",
    instructions="Given a lead JSON, return a total installed price in GBP.",
    model="gpt-4o-mini",
    model_settings=ModelSettings(
        temperature=0,
    ),
    tools=[price_sheet],
)