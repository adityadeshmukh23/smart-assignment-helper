# Prompts Used in Smart Assignment Helper

This document contains all LLM prompts used in the Smart Assignment Helper system for reproducibility and transparency.

---

## 1. Planner Prompt

**Role:** Generate structured plan from assignment description

**Prompt Template:**

```
You are PLANNER. Input is an assignment description. Output ONLY valid JSON with fields:
{
  "objective":"<one-line summary of assignment goal>",
  "milestones":[
     {"id":1,"title":"<milestone title>","tasks":[{"id":"1.1","desc":"<task description>"}],"est_hours":<int>}
     ...
  ],
  "deliverables":["README.md","system_design.md","source_code"],
  "notes":"<constraints or clarifications>"
}
Make JSON minimal and parseable.

Assignment Description:
{assignment_text}
```

**Parameters:**
- Model: `gpt-4o-mini`
- Temperature: `0.2`
- Max Tokens: `800`

**Example Output:**
```json
{
  "objective": "Build a 2-page system design and implement MVP for assignment helper",
  "milestones": [
    {
      "id": 1,
      "title": "System Design",
      "tasks": [
        {"id": "1.1", "desc": "Create system_design.md with architecture"},
        {"id": "1.2", "desc": "Document requirements and data schema"}
      ],
      "est_hours": 3
    },
    {
      "id": 2,
      "title": "Implementation",
      "tasks": [
        {"id": "2.1", "desc": "Build Streamlit UI"},
        {"id": "2.2", "desc": "Implement LLM client wrapper"},
        {"id": "2.3", "desc": "Create Planner and Executor agents"}
      ],
      "est_hours": 5
    }
  ],
  "deliverables": ["README.md", "system_design.md", "frontend/app.py", "tools/llm_client.py"],
  "notes": "Ensure all LLM interactions are logged for transparency"
}
```

---

## 2. Executor Prompt

**Role:** Execute individual tasks from plan and generate outputs

**Prompt Template:**

```
You are EXECUTOR. Input: a single task (text) and current context (assignment brief + previous outputs).

Return JSON:
{
  "action": "Generate_File" | "RAG_Search" | "NoOp",
  "filename": "README.md",
  "content": "<full content for file>",
  "meta": {
    "sources": [
      {"title": "<source title>", "url": "<source url>", "snippet": "<relevant excerpt>"}
    ]
  }
}

If action is RAG_Search, return top 3 passages with source links.
If action is Generate_File, provide complete file content.

Context:
Assignment: {assignment_text}
Task: {task_description}
Previous Outputs: {previous_outputs}
```

**Parameters:**
- Model: `gpt-4o-mini`
- Temperature: `0.2`
- Max Tokens: `800`

**Example Output (Generate_File):**
```json
{
  "action": "Generate_File",
  "filename": "README.md",
  "content": "# Smart Assignment Helper\n\nAI-powered tool to analyze assignments, generate plans, and create deliverables.\n\n## Features\n- Plan generation\n- File creation\n- RAG-based resource retrieval\n\n## Usage\n```bash\nstreamlit run frontend/app.py\n```",
  "meta": {
    "sources": []
  }
}
```

**Example Output (RAG_Search):**
```json
{
  "action": "RAG_Search",
  "filename": "",
  "content": "",
  "meta": {
    "sources": [
      {
        "title": "Machine Learning Course Notes - Lecture 5",
        "url": "https://example.com/ml-notes/lecture5.pdf",
        "snippet": "Neural networks consist of layers of interconnected nodes..."
      },
      {
        "title": "System Design Principles",
        "url": "https://example.com/system-design.pdf",
        "snippet": "Scalability requires careful consideration of data flow..."
      },
      {
        "title": "Assignment Best Practices",
        "url": "https://example.com/best-practices.md",
        "snippet": "Always start with a clear problem statement and requirements..."
      }
    ]
  }
}
```

---

## 3. Few-Shot Examples (Optional Enhancement)

For improved prompt performance, include 1-2 few-shot examples directly in the prompt:

### Planner Few-Shot Example

**Input:**
```
Assignment: Build a simple web scraper to extract product prices from e-commerce sites. Create documentation and unit tests.
```

**Output:**
```json
{
  "objective": "Build web scraper with documentation and tests",
  "milestones": [
    {"id": 1, "title": "Core Implementation", "tasks": [{"id": "1.1", "desc": "Write scraper script"}, {"id": "1.2", "desc": "Handle rate limiting"}], "est_hours": 2},
    {"id": 2, "title": "Testing & Docs", "tasks": [{"id": "2.1", "desc": "Write unit tests"}, {"id": "2.2", "desc": "Create README"}], "est_hours": 2}
  ],
  "deliverables": ["scraper.py", "tests/", "README.md"],
  "notes": "Follow robots.txt guidelines"
}
```

---

## 4. Prompt Engineering Notes

### Best Practices Applied

1. **Clear Role Definition:** "You are PLANNER" / "You are EXECUTOR"
2. **Output Format Specification:** "Output ONLY valid JSON"
3. **Schema Enforcement:** Explicitly define expected JSON structure
4. **Temperature Control:** Use low temperature (0.2) for structured outputs
5. **Token Limits:** Set appropriate max_tokens to control response length
6. **Few-Shot Learning:** Include examples when needed for consistency

### Common Issues & Solutions

- **Issue:** LLM returns text instead of JSON
  - **Solution:** Emphasize "Output ONLY valid JSON" and provide explicit schema

- **Issue:** Malformed JSON with extra text
  - **Solution:** Add few-shot examples showing clean JSON output

- **Issue:** Incomplete or truncated responses
  - **Solution:** Increase max_tokens or simplify output requirements

---

## 5. Future Prompt Extensions

### Critic Agent (Planned)
**Role:** Review and improve generated plans and outputs

```
You are CRITIC. Review the following plan and suggest improvements.
Focus on: completeness, feasibility, time estimates, missing dependencies.

Plan:
{plan_json}

Provide feedback as JSON:
{
  "issues": [{"severity": "high|medium|low", "description": "..."}],
  "suggestions": ["..."]
}
```

### RAG Query Generator (Planned)
**Role:** Convert task into optimal search queries for RAG

```
You are QUERY_GENERATOR. Convert task into 3 search queries for RAG retrieval.

Task: {task_description}

Return JSON:
{
  "queries": ["query1", "query2", "query3"]
}
```

---

## 6. Versioning

| Version | Date | Changes |
|---------|------|----------|
| v1.0 | 2025-11-03 | Initial prompts for Planner and Executor |
| v1.1 | TBD | Add few-shot examples |
| v2.0 | TBD | Add Critic and RAG query generator |

---

**Last Updated:** November 03, 2025  
**Maintained By:** Aditya Deshmukh (adityad23@iitk.ac.in)
