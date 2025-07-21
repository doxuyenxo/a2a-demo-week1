from fastapi import FastAPI, Request
import uvicorn
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from shared.gemini_client import classify_intent_with_gemini, get_agent_by_intent
from shared.gprc_client import call_agent

app = FastAPI()


@app.post("/prompt")
async def handle_promt(req: Request):
    data = await req.json()
    promt = data["prompt"]
    intent = classify_intent_with_gemini(promt)
    agent_info = get_agent_by_intent(intent)
    if agent_info is None:
        return {"error": "No agent matched or not found"}
    result = call_agent(agent_info["host"], promt)
    return {"result": result}

def start_server():
    uvicorn.run("agent_host.__main__:app")

if __name__ == "__main__":
    start_server()