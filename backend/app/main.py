# backend/app/main.py
from fastapi import FastAPI, WebSocket, Depends, WebSocketDisconnect
from sqlmodel import Session
from agents import Runner
from .lead_agent import lead_agent
from .db import engine, get_session
from .models import SQLModel, Lead

app = FastAPI()

# Create all tables on startup.  This will create the `lead` table in Postgres.
SQLModel.metadata.create_all(engine)


@app.get("/", include_in_schema=False)
def root():
    return {"status": "ok"}


@app.get("/healthz", include_in_schema=False)
def healthz():
    return {"ok": True}


def save_lead(data: dict, session: Session):
    """
    Given a dict with keys exactly matching LeadIn (name, email, postcode, product_type),
    persist it to Postgres.  Return the created Lead instance if needed.
    """
    lead = Lead(**data)
    session.add(lead)
    session.commit()
    return lead


@app.websocket("/chat")
async def chat(ws: WebSocket, session: Session = Depends(get_session)):
    await ws.accept()
    history: list[dict] = []

    try:
        while True:
            # 1) Wait for the next user message
            user_msg = await ws.receive_text()
            history.append({"role": "user", "content": user_msg})

            # 2) Run the "Lead-Collector" agent on the full conversation history
            result = await Runner.run(lead_agent, history)

            # 3) Check for any create_lead tool call
            created_a_lead = False
            for item in result.new_items:
                # ToolCallItem has a `.tool_name` attribute for function-tool name
                if hasattr(item, "tool_name") and item.tool_name == "create_lead":
                    lead_payload = item.args.get("lead", {})
                    # Persist it immediately
                    save_lead(lead_payload, session)
                    created_a_lead = True
                    break

            # 4) Decide what text to send back to the user
            if created_a_lead:
                final_text = "Great – we’ve saved your info. Local installers will bid on your custom system soon!"
            else:
                # If there was no create_lead call, just send whatever the agent said
                final_text = result.final_output or ""

            # 5) Append the assistant’s response to history so the next turn has context
            history.append({"role": "assistant", "content": final_text})

            # 6) Send that text back over the WebSocket
            await ws.send_text(final_text)

    except WebSocketDisconnect:
        # Client closed connection.  Just return cleanly.
        return