from fastapi import FastAPI, WebSocket, Depends, WebSocketDisconnect
from sqlmodel import Session
from agents import Runner
from agents.items import ToolCallItem

from .lead_agent import lead_agent
from .db import engine, get_session
from .models import SQLModel, Lead

app = FastAPI()
SQLModel.metadata.create_all(engine)

@app.get("/", include_in_schema=False)
def root():
    return {"status": "ok"}

@app.get("/healthz", include_in_schema=False)
def healthz():
    return {"ok": True}

def save_lead(data: dict, session: Session):
    """
    Persist the lead into Postgres (or whatever DATABASE_URL is pointing to).
    """
    lead = Lead(**data)
    session.add(lead)
    session.commit()
    return lead

@app.websocket("/chat")
async def chat(ws: WebSocket, session: Session = Depends(get_session)):
    await ws.accept()
    history: list[dict[str, str]] = []

    try:
        while True:
            # 1) Receive next user message
            user_msg = await ws.receive_text()
            history.append({"role": "user", "content": user_msg})

            # 2) Run our Lead‐Collector + Solar‐Info agent
            result = await Runner.run(lead_agent, history)

            # 3) Look for any ToolCallItem where tool_name == "create_lead"
            created_a_lead = False
            for item in result.new_items:
                if isinstance(item, ToolCallItem) and item.tool_name == "create_lead":
                    # The agent has assembled all required fields into item.args["lead"]
                    lead_payload = item.args["lead"]
                    save_lead(lead_payload, session)
                    created_a_lead = True
                    break

            # 4) Decide what to send back
            if created_a_lead:
                final_text = "Great – we’ve saved your info and local installers will bid soon! 🙌"
            else:
                final_text = result.final_output

            # 5) Append the assistant’s reply to history & send it over WebSocket
            history.append({"role": "assistant", "content": final_text})
            await ws.send_text(final_text)

    except WebSocketDisconnect:
        # Client disconnected – clean exit
        returnal_output or ""

            # 5) Append the assistant’s response to history so the next turn has context
            history.append({"role": "assistant", "content": final_text})

            # 6) Send that text back over the WebSocket
            await ws.send_text(final_text)

    except WebSocketDisconnect:
        # Client closed connection.  Just return cleanly.
        return