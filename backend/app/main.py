# backend/app/main.py
from fastapi import FastAPI, WebSocket, Depends
from sqlmodel import Session
from agents import Runner
from .lead_agent import lead_agent
from .db import engine, get_session
from .models import SQLModel, Lead

app = FastAPI()
SQLModel.metadata.create_all(engine)

# Responds to GET / with 200 OK
@app.get("/", include_in_schema=False)
def root():
    return {"status": "ok"}

# Responds to GET /healthz with 200 OK
@app.get("/healthz", include_in_schema=False)
def healthz():
    return {"ok": True}

def save_lead(data: dict, session: Session):
    lead = Lead(**data)
    session.add(lead)
    session.commit()
    return lead

@app.websocket("/chat")
async def chat(ws: WebSocket, session: Session = Depends(get_session)):
    await ws.accept()
    history = []  # this will be a list of {"role": "...", "content": "..."} dicts

    while True:
        user_msg = await ws.receive_text()
        history.append({"role": "user", "content": user_msg})

        # ❌ remove: agent_msg = lead_agent.run(history)
        # ✅ use Runner.run(...) to actually execute the agent
        result = await Runner.run(lead_agent, history)

        # If the agent called our `create_lead` tool, it will show up in result.new_items
        # We can inspect result.new_items for a ToolCallItem whose .name == "create_lead"
        # For simplicity, let's look for any tool call named "create_lead"
        created_a_lead = False
        for item in result.new_items:
            if item.type == "tool_call_item" and item.name == "create_lead":
                # Grab the arguments that the agent is passing to create_lead
                lead_payload = item.args["lead"]
                save_lead(lead_payload, session)
                created_a_lead = True
                break

        if created_a_lead:
            # If we ran create_lead, send a confirmation message back
            final_text = "Great – we've sent your spec for quoting. Expect prices soon!"
        else:
            # Otherwise, just send whatever the agent's final_output was
            final_text = result.final_output

        # Append the agent’s response to the history so that the next turn includes it
        history.append({"role": "assistant", "content": final_text})
        await ws.send_text(final_text)