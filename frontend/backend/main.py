# backend/main.py
# Minimal FastAPI backend with health, planner, and executor endpoints.
# Not required by the Streamlit UI (it talks to OpenAI directly),
# but useful if you want to separate concerns or extend tools later.

import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict

from tools.llm_client import LLMClient, build_planner_prompt, build_executor_prompt

app = FastAPI(title="Smart Assignment Helper Backend", version="0.1.0")

# Instantiate once
try:
    llm = LLMClient(model=os.getenv("SAH_MODEL", "gpt-4o-mini"))
except Exception as e:
    # Defer failure until first call; allow /health to still respond
    llm = None
    _startup_error = str(e)
else:
    _startup_error = None


class PlanRequest(BaseModel):
    assignment: str

class ExecuteRequest(BaseModel):
    assignment: str
    task_desc: str
    context: str | None = None


@app.get("/health")
def health() -> Dict[str, Any]:
    return {
        "status": "ok" if _startup_error is None else "degraded",
        "model": os.getenv("SAH_MODEL", "gpt-4o-mini"),
        "startup_error": _startup_error
    }


@app.post("/planner")
def planner(req: PlanRequest) -> Dict[str, Any]:
    if not req.assignment.strip():
        raise HTTPException(status_code=400, detail="Empty assignment.")
    try:
        client = llm or LLMClient(model=os.getenv("SAH_MODEL", "gpt-4o-mini"))
        resp = client.chat(build_planner_prompt(req.assignment))
        # Ensure valid JSON
        plan = json.loads(resp)
        return {"plan": plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Planner error: {e}") from e


@app.post("/executor")
def executor(req: ExecuteRequest) -> Dict[str, Any]:
    if not req.task_desc.strip():
        raise HTTPException(status_code=400, detail="Empty task_desc.")
    try:
        client = llm or LLMClient(model=os.getenv("SAH_MODEL", "gpt-4o-mini"))
        resp = client.chat(build_executor_prompt(req.task_desc, req.assignment, req.context or ""))
        ex = json.loads(resp)
        return {"result": ex}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Executor error: {e}") from e
