from fastapi import FastAPI, WebSocket, Depends
from sqlmodel import Session
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
    history = []
    while True:
        user_msg = await ws.receive_text()
        history.append({"role": "user", "content": user_msg})

        agent_msg = lead_agent.run(history)

        # inside chat() loop
        if agent_msg.tool_call and agent_msg.tool_call.name == "create_lead":
            lead_payload = agent_msg.tool_call.args["lead"]
            save_lead(lead_payload, session)
            agent_msg = agent_msg.confirm(
                "Great – we've sent your spec for quoting. Expect prices soon!"
            )

        history.append(agent_msg.to_dict())
        await ws.send_text(agent_msg.content)