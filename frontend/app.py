# frontend/app.py
# Streamlit MVP: Paste assignment -> Planner (JSON) -> Run first/selected task via Executor
# Saves interaction logs to interaction_logs/interactions.jsonl
# Optional: edit plan JSON in-place and re-run.

import os
import json
import datetime as dt
from typing import Dict, Any, List

import streamlit as st

# Local imports
from tools.llm_client import LLMClient, build_planner_prompt, build_executor_prompt

# ---- Setup ----
st.set_page_config(page_title="Smart Assignment Helper", page_icon="🧠", layout="centered")
st.title("🧠 Smart Assignment Helper — MVP")

os.makedirs("interaction_logs", exist_ok=True)
LOG_FILE = "interaction_logs/interactions.jsonl"

# Create LLM client (errors show nicely in UI)
@st.cache_resource(show_spinner=False)
def get_client():
    return LLMClient(model=os.getenv("SAH_MODEL", "gpt-4o-mini"), temperature=0.2)

# ---- Small helpers ----
def save_log(entry: Dict[str, Any]):
    entry["ts"] = dt.datetime.utcnow().isoformat() + "Z"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def pretty_json(obj: Any) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False)

# ---- UI: Input ----
st.subheader("1) Paste your assignment / brief")
assignment_text = st.text_area("Assignment brief", height=220, placeholder="Paste the task here…")

colA, colB = st.columns([1,1])
with colA:
    do_plan = st.button("✨ Generate Plan (Planner)")
with colB:
    clear = st.button("Clear")

if clear:
    st.experimental_rerun()

# ---- Planner call ----
if do_plan:
    if not assignment_text.strip():
        st.warning("Please paste the assignment first.")
        st.stop()
    try:
        client = get_client()
        with st.spinner("Thinking (Planner)…"):
            planner_resp = client.chat(build_planner_prompt(assignment_text))
        st.caption("Raw Planner JSON:")
        st.code(planner_resp, language="json")

        # Try to parse JSON; if it fails, allow manual fix.
        try:
            plan = json.loads(planner_resp)
        except Exception as e:
            st.error("Planner returned invalid JSON. You can edit and fix below, then click 'Use Edited Plan'.")
            edited = st.text_area("Edit plan JSON", value=planner_resp, height=260)
            if st.button("Use Edited Plan"):
                try:
                    plan = json.loads(edited)
                except Exception as e2:
                    st.stop()
            else:
                st.stop()

        # Persist in session
        st.session_state["plan"] = plan
        st.success("Plan parsed successfully ✅")
        save_log({
            "phase": "planner",
            "assignment": assignment_text,
            "planner_output": plan
        })
    except Exception as e:
        st.error(f"Planner error: {e}")
        st.stop()

# ---- Display & Execute ----
plan = st.session_state.get("plan")
if plan:
    st.subheader("2) Review / Edit Plan")
    # Show as editable JSON text (safer than dict editor)
    plan_text = st.text_area("Plan JSON (editable)", value=pretty_json(plan), height=300)
    if st.button("💾 Save Edited Plan"):
        try:
            plan = json.loads(plan_text)
            st.session_state["plan"] = plan
            st.success("Plan updated.")
        except Exception as e:
            st.error(f"Invalid JSON: {e}")

    st.subheader("3) Execute tasks")
    # Flatten tasks with ids for simple selection
    task_items: List[Dict[str, str]] = []
    for m in plan.get("milestones", []):
        for t in m.get("tasks", []):
            task_items.append({
                "label": f'{m.get("id")}.{t.get("id")} — {t.get("desc")}',
                "desc": t.get("desc", ""),
                "mid": m.get("id"),
                "tid": t.get("id")
            })

    if not task_items:
        st.info("No tasks found in plan.")
    else:
        labels = [x["label"] for x in task_items]
        idx = st.selectbox("Select a task to execute", list(range(len(labels))), format_func=lambda i: labels[i])
        chosen = task_items[idx]
        st.write("**Chosen task:**", chosen["desc"])

        if st.button("▶️ Run Executor for this task"):
            try:
                client = get_client()
                with st.spinner("Running (Executor)…"):
                    exec_resp = client.chat(build_executor_prompt(chosen["desc"], assignment_text))
                st.caption("Raw Executor JSON:")
                st.code(exec_resp, language="json")

                try:
                    ex = json.loads(exec_resp)
                except Exception as e:
                    st.error(f"Executor returned invalid JSON: {e}")
                    st.stop()

                action = ex.get("action", "NoOp")
                if action == "Generate_File":
                    filename = ex.get("filename", "output.txt")
                    content = ex.get("content", "")
                    # Ensure path is within repo root for safety
                    safe_name = filename.replace("..", "").strip().lstrip("/")
                    with open(safe_name, "w", encoding="utf-8") as fh:
                        fh.write(content)
                    st.success(f"File generated: `{safe_name}`")
                    st.download_button("⬇️ Download file", data=content, file_name=safe_name)
                elif action == "NoOp":
                    st.info("No operation suggested for this task.")
                else:
                    st.info(f"Unhandled action: {action}")

                save_log({
                    "phase": "executor",
                    "assignment": assignment_text,
                    "task": chosen,
                    "executor_output": ex
                })

            except Exception as e:
                st.error(f"Executor error: {e}")

    st.divider()
    st.subheader("4) Deliverables checklist")
    st.write("- [x] Planner JSON")
    st.write("- [x] Executor generated files (e.g., README.md, Solution.java)")
    st.write("- [x] Interaction logs saved to `interaction_logs/interactions.jsonl`")

st.caption("Tip: set OPENAI_API_KEY in your environment before running. Example:")
st.code('export OPENAI_API_KEY="sk-..."', language="bash")
