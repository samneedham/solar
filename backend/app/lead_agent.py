from agents import Agent, ModelSettings
from .tools import create_lead

lead_agent = Agent(
    name="Solar-Guide-And-Lead-Collector",
    instructions=(
        "You are a friendly, expert solar energy assistant. "
        "You can answer any questions about solar technology, benefits, costs, finance options, etc. "
        "If at any point the user asks for 'a solar quote' or 'design me a system' or otherwise indicates "
        "they want to move forward, you should gather exactly these pieces of