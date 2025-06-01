# backend/app/main.py
from fastapi import FastAPI, WebSocket, Depends, WebSocketDisconnect
from sqlmodel import Session
from agents import Runner, ToolCallItem
from .lead_agent import lead_agent
from .db import engine, get_session
from .models import SQLModel, Lead

app = FastAPI()
SQLModel.metadata.create_all(engine)  # Create the Lead table on startup

@app.get("/", include_in_schema=False)
def root():
    return {"status": "ok"}

@app.get("/healthz", include_in_schema=False)
def healthz():
    return {"ok": True}

def save_lead(data: dict, session: Session):
    # data is guaranteed to match LeadIn {name, email, postcode, product_type}
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
            # 1) Receive user message
            user_msg = await ws.receive_text()
            history.append({"role": "user", "content": user_msg})

            # 2) Run the Lead-Collector agent on the full history
            result = await Runner.run(lead_agent, history)

            # 3) Look for a create_lead tool call
            created_a_lead = False
            for item in result.new_items:
                # Check that 'item' is a ToolCallItem and that its tool name is "create_lead"
                if isinstance(item, ToolCallItem) and item.tool.name == "create_lead":
                    lead_payload: dict = item.args["lead"]
                    save_lead(lead_payload, session)
                    created_a_lead = True
                    break

            # 4) Decide what text to send back
            if created_a_lead:
                final_text = "Great — we’ve saved your info. Local installers will bid soon!"
            else:
                final_text = result.final_output

            # 5) Append bot’s reply to history & send via WebSocket
            history.append({"role": "assistant", "content": final_text})
            await ws.send_text(final_text)

    except WebSocketDisconnect:
        # The client closed the socket; exit cleanly
        return