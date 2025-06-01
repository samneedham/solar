# backend/app/main.py

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
    lead = Lead(**data)
    session.add(lead)
    session.commit()
    return lead


@app.websocket("/chat")
async def chat(ws: WebSocket, session: Session = Depends(get_session)):
    await ws.accept()
    history = []

    try:
        while True:
            # 1) Receive the next user message
            user_msg = await ws.receive_text()
            history.append({"role": "user", "content": user_msg})

            # 2) Run our “Solar‐info + Lead‐Collector” agent
            result = await Runner.run(lead_agent, history)

            # 3) Check for a create_lead tool call in result.new_items
            created_a_lead = False
            for item in result.new_items:
                if isinstance(item, ToolCallItem) and item.tool_name == "create_lead":
                    lead_payload = item.args["lead"]
                    save_lead(lead_payload, session)
                    created_a_lead = True
                    break

            # 4) Decide what to send back
            if created_a_lead:
                final_text = "Great – we’ve saved your info and local installers will bid soon!"
            else:
                final_text = result.final_output

            # 5) Append the assistant’s reply to history & send it
            history.append({"role": "assistant", "content": final_text})
            await ws.send_text(final_text)

    except WebSocketDisconnect:
        # Client disconnected – cleanly exit
        return