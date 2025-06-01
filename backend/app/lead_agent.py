from agents import Agent, Guardrail
from .tools import create_lead

email_guard = Guardrail(
    name="email_required",
    check=lambda s: s.get("email") is not None,
    on_fail="ask",
)

lead_agent = Agent(
    name="Lead-Collector",
    instructions=(
        "You are a friendly assistant matching homeowners with installers. "
        "Ask as few questions as possible to fill the create_lead tool."
    ),
    tools=[create_lead],
    guardrails=[email_guard],
    model_config={"model": "gpt-4o-mini"},   # ultra-fast public landing page
)