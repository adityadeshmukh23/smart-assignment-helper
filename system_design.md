# Smart Assignment Helper - System Design

**Author:** Aditya Deshmukh  
**Roll No:** 230066  
**Institution:** IIT Kanpur, Materials Science and Engineering  
**Email:** adityad23@iitk.ac.in

---

## 1. Problem Statement

Students often face challenges in breaking down complex assignment descriptions into actionable tasks, organizing their work, and finding relevant resources. The **Smart Assignment Helper** addresses this by providing an AI-powered system that:

- Analyzes assignment briefs and extracts key objectives
- Generates structured plans with milestones and tasks
- Executes tasks to produce deliverables (README, code skeletons, documentation)
- Retrieves relevant resources via RAG (Retrieval-Augmented Generation)
- Logs all interactions for transparency and reproducibility

---

## 2. Requirements

### 2.1 Functional Requirements

- **FR1:** Accept natural language assignment descriptions as input
- **FR2:** Generate structured JSON plans with objectives, milestones, tasks, and deliverables
- **FR3:** Execute tasks to create files (README.md, code skeletons, documentation)
- **FR4:** Retrieve relevant resources from a knowledge corpus using RAG
- **FR5:** Allow users to edit and re-run plans through the UI
- **FR6:** Log all LLM interactions with timestamps in JSONL format
- **FR7:** Save all prompts used for reproducibility

### 2.2 Non-Functional Requirements

- **NFR1:** Response time < 10 seconds for plan generation
- **NFR2:** Support for OpenAI GPT-4o-mini or compatible LLM APIs
- **NFR3:** Clean, intuitive Streamlit-based UI
- **NFR4:** Modular architecture enabling easy extension
- **NFR5:** Comprehensive logging for audit and debugging

---

## 3. System Architecture

### 3.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      User Interface                         │
│                    (Streamlit Web App)                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   Application Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Planner    │  │   Executor   │  │   Logger     │     │
│  │   Agent      │  │   Agent      │  │   Module     │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│                     Service Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  LLM Client  │  │  RAG Engine  │  │ File System  │     │
│  │  (OpenAI)    │  │  (ChromaDB)  │  │   Storage    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Component Descriptions

#### **Frontend (Streamlit Web App)**
- Single-page application for user interaction
- Input: Text area for assignment description
- Output: Displays JSON plan, execution results, generated files
- Actions: "Plan & Generate", "Edit Plan", "Execute Task", "Include RAG"

#### **Planner Agent**
- **Role:** Analyzes assignment and produces structured plan
- **Input:** Assignment description (free text)
- **Output:** JSON with objectives, milestones, tasks, deliverables, notes
- **LLM Prompt:** System prompt defines JSON schema and few-shot examples

#### **Executor Agent**
- **Role:** Executes individual tasks from the plan
- **Actions:**
  - `Generate_File`: Creates README, code skeletons, documentation
  - `RAG_Search`: Retrieves top-k relevant passages from corpus
  - `NoOp`: Placeholder for future actions
- **Input:** Single task description + context
- **Output:** JSON with action, filename, content, metadata

#### **LLM Client (tools/llm_client.py)**
- Wrapper for OpenAI API calls
- Handles authentication via environment variable `OPENAI_API_KEY`
- Configurable parameters: model, temperature, max_tokens
- Returns raw LLM response text

#### **RAG Engine (Optional - Future Enhancement)**
- Embeddings: OpenAI `text-embedding-ada-002` or open-source alternatives
- Vector Database: ChromaDB (local) or FAISS
- Corpus: Lecture notes, sample assignments, documentation (stored in `corpus/`)
- Retrieval: Top-k similar passages with source citations

#### **Logger Module**
- Writes interactions to `interaction_logs/interactions.jsonl`
- Format: One JSON object per line with timestamp, prompts, responses
- Saves prompts to `interaction_logs/prompts_used.md` for reproducibility

#### **File System Storage**
- Stores generated files (README.md, Solution.java, etc.)
- Organizes outputs in project directory
- Future: Auto-commit to Git branch

---

## 4. Data Schema

### 4.1 Plan Schema (JSON)

```json
{
  "objective": "string",
  "milestones": [
    {
      "id": 1,
      "title": "string",
      "tasks": [
        {
          "id": "1.1",
          "desc": "string"
        }
      ],
      "est_hours": 2
    }
  ],
  "deliverables": ["README.md", "system_design.md", "source_code"],
  "notes": "string"
}
```

### 4.2 Executor Output Schema (JSON)

```json
{
  "action": "Generate_File | RAG_Search | NoOp",
  "filename": "string",
  "content": "string",
  "meta": {
    "sources": [
      {
        "title": "string",
        "url": "string",
        "snippet": "string"
      }
    ]
  }
}
```

### 4.3 Interaction Log Schema (JSONL)

```json
{
  "timestamp": "2025-11-03T13:00:00Z",
  "assignment": "string",
  "planner_prompt": "string",
  "planner_response": {},
  "executor_calls": [
    {
      "task_id": "1.1",
      "executor_prompt": "string",
      "executor_response": {}
    }
  ]
}
```

---

## 5. Security & Privacy Measures

- **API Key Management:** Store `OPENAI_API_KEY` in environment variables, never in code
- **Input Validation:** Sanitize user inputs to prevent injection attacks
- **Rate Limiting:** Implement client-side throttling to avoid API abuse
- **Data Privacy:** Do not log sensitive personal information; anonymize logs if needed
- **Access Control:** Future: Add authentication for multi-user deployments

---

## 6. Dependencies & Technologies

| Component | Technology | Purpose |
|-----------|------------|----------|
| Frontend | Streamlit | Web UI framework |
| LLM API | OpenAI GPT-4o-mini | Natural language processing |
| Vector DB (future) | ChromaDB / FAISS | RAG-based retrieval |
| Logging | Python logging + JSONL | Interaction tracking |
| Language | Python 3.9+ | Core implementation |
| Code Generation | Templates | Java/Python skeleton generation |

---

## 7. How to Run

### 7.1 Setup

```bash
# Clone repository
git clone <repo-url>
cd smart-assignment-helper

# Install dependencies
pip install -r requirements.txt

# Set OpenAI API key
export OPENAI_API_KEY="sk-..."
```

### 7.2 Run Application

```bash
streamlit run frontend/app.py
```

### 7.3 Usage Flow

1. Paste assignment description in text area
2. Click "Plan & Generate" to invoke Planner
3. Review generated JSON plan
4. Click "Run first task" to execute with Executor
5. View generated files (README.md, code skeletons)
6. Check `interaction_logs/interactions.jsonl` for logs

---

## 8. Limitations & Future Work

### Current Limitations

- Single-user application (no multi-tenancy)
- No persistent database (logs stored as files)
- Limited error handling for malformed LLM outputs
- RAG not yet implemented (planned for next phase)
- Manual task execution (no automated workflow engine)

### Future Enhancements

1. **Multi-Agent Orchestration:** Implement supervisor agent for complex workflows
2. **RAG Integration:** Index course materials and enable semantic search
3. **Automated Git Commits:** Executor creates branches and commits generated files
4. **Web-based Plan Editor:** Drag-and-drop task reordering, milestone editing
5. **Template Library:** Pre-built templates for common assignment types
6. **Collaboration Features:** Share plans and generated artifacts with peers
7. **Evaluation Metrics:** Track plan quality, task completion rates

---

## 9. Evaluation Checklist

- [x] Demonstrates reasoning (Planner extracts objectives)
- [x] Demonstrates planning (Structured milestones and tasks)
- [x] Demonstrates execution (Generates files)
- [x] Clean UI with Streamlit
- [x] Interaction logs in JSONL format
- [x] Prompts saved for reproducibility
- [x] System design documented
- [ ] RAG implemented (future work)
- [ ] Demo video recorded (in progress)

---

## 10. Contact

**Aditya Deshmukh**  
Roll No: 230066  
IIT Kanpur, Materials Science and Engineering  
Email: adityad23@iitk.ac.in  
GitHub: [adityadeshmukh23](https://github.com/adityadeshmukh23)

---

*Last Updated: November 03, 2025*
