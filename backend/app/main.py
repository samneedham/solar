# backend/app/main.py

from fastapi import FastAPI, WebSocket, Depends, WebSocketDisconnect
from sqlmodel import Session
from agents import Runner
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
    history: list[dict] = []

    try:
        while True:
            # if the client closes, receive_text() will raise WebSocketDisconnect
            user_msg = await ws.receive_text()
            history.append({"role": "user", "content": user_msg})

            # Run the Lead‐Collector agent
            result = await Runner.run(lead_agent, history)

            # Look for a create_lead tool call
            lead_saved = False
            for item in result.new_items:
                if item.type == "tool_call_item" and item.name == "create_lead":
                    lead_payload = item.args["lead"]
                    save_lead(lead_payload, session)
                    lead_saved = True
                    break

            if lead_saved:
                confirmation = "Great – we've sent your spec for quoting. Expect prices soon!"
                history.append({"role": "assistant", "content": confirmation})
                await ws.send_text(confirmation)

                # (Optionally chain to bid_agent here)
            else:
                reply = result.final_output
                history.append({"role": "assistant", "content": reply})
                await ws.send_text(reply)

    except WebSocketDisconnect:
        # Client disconnected—just exit the loop cleanly
        print("⏹️ WebSocket disconnected by client")
        return