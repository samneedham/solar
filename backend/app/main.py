# backend/app/main.py
from fastapi import FastAPI, WebSocket, Depends, WebSocketDisconnect
from sqlmodel import Session
from agents import Runner
from .lead_agent import lead_agent
from .db import engine, get_session
from .models import SQLModel, Lead

app = FastAPI()
SQLModel.metadata.create_all(engine)  # Create tables on startup

@app.get("/", include_in_schema=False)
def root():
    return {"status": "ok"}

@app.get("/healthz", include_in_schema=False)
def healthz():
    return {"ok": True}

def save_lead(data: dict, session: Session):
    # data matches LeadIn: {name, email, postcode, product_type}
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
            # 1) Get the next user message
            user_msg = await ws.receive_text()
            history.append({"role": "user", "content": user_msg})

            # 2) Run the “Lead-Collector” agent on the full history
            result = await Runner.run(lead_agent, history)

            # 3) Check if the agent invoked create_lead
            created_a_lead = False
            for item in result.new_items:
                if item.type == "tool_call_item" and item.name == "create_lead":
                    # Unpack the JSON that the LLM produced:
                    lead_payload: dict = item.args["lead"]
                    save_lead(lead_payload, session)
                    created_a_lead = True
                    break

            # 4) Decide what to send back
            if created_a_lead:
                final_text = "Great — we’ve saved your info. Local installers will bid soon!"
            else:
                # No tool call → LLM is asking a follow-up or giving info
                final_text = result.final_output

            # 5) Append the bot’s reply to history & send to client
            history.append({"role": "assistant", "content": final_text})
            await ws.send_text(final_text)

    except WebSocketDisconnect:
        # Client closed connection; exit gracefully
        return