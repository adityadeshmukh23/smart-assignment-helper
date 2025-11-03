# tools/llm_client.py
# Simple LLM wrapper (OpenAI SDK v1.x). Reads OPENAI_API_KEY from env.
# Returns assistant text content and raises on errors, so callers can handle.

import os
from typing import List, Dict, Any, Optional

try:
    from openai import OpenAI
except Exception as e:
    raise RuntimeError(
        "OpenAI SDK not found. Install with: pip install openai"
    ) from e


class LLMClient:
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.2):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "OPENAI_API_KEY is not set. Export it before running the app."
            )
        self.client = OpenAI()
        self.model = model
        self.temperature = temperature

    def chat(self, messages: List[Dict[str, str]], max_tokens: int = 1200) -> str:
        """
        messages: [{"role":"user"|"system"|"assistant","content":"..."}]
        returns assistant message content (str)
        """
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content


# ---- Helper prompt builders (Planner & Executor) ----

def build_planner_prompt(assignment_text: str) -> List[Dict[str, str]]:
    system = (
        "You are PLANNER, a strict JSON-only planner agent. "
        "Given an assignment brief, output ONLY valid JSON with keys: "
        "`objective` (string), `milestones` (list of objects with {id:int,title:string,"
        "est_hours:int,tasks:[{id:string,desc:string}]}), `deliverables` (list), `notes` (string). "
        "Do not include comments or extra prose."
    )
    user = f"""Assignment Brief:
\"\"\"{assignment_text}\"\"\"

Respond ONLY with JSON. Example of shape:
{{
  "objective": "one-line",
  "milestones": [
    {{"id":1,"title":"Understand problem","est_hours":1,"tasks":[{{"id":"1.1","desc":"Extract requirements"}}]}},
    {{"id":2,"title":"Design","est_hours":2,"tasks":[{{"id":"2.1","desc":"Write system design"}}]}}
  ],
  "deliverables": ["README.md","system_design.md","source_code"],
  "notes": "constraints or assumptions"
}}
"""
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def build_executor_prompt(task_desc: str, assignment_text: str, context: Optional[str] = "") -> List[Dict[str, str]]:
    system = (
        "You are EXECUTOR. You perform ONE task and return actionable JSON. "
        "Choose an action from: Generate_File, NoOp. "
        "For Generate_File, include `filename` and full `content` (complete file text). "
        "Respond with ONLY JSON."
    )
    user = f"""Task: {task_desc}
Assignment context:
\"\"\"{assignment_text}\"\"\"

If the task suggests writing README or a skeleton file, produce it.
Return JSON like:
{{
  "action": "Generate_File",
  "filename": "README.md",
  "content": "# Title\\n..."
}}
If nothing to do, return: {{ "action":"NoOp" }}.

Additional context (optional):
{context or "N/A"}
"""
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]
