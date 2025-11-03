# Demo Screenshots and Videos

This directory contains demo materials for the Smart Assignment Helper project.

## Contents

### Screenshots

Screenshots will be added here to demonstrate:

1. **UI Overview** - Main Streamlit interface
   - Assignment input text area
   - Plan & Generate button
   - Plan display section

2. **Plan Generation** - JSON plan output
   - Structured milestones and tasks
   - Deliverables list
   - Time estimates

3. **Task Execution** - File generation results
   - Generated README.md
   - Code skeletons (e.g., Solution.java)
   - Execution logs

4. **RAG Integration (Future)** - Resource retrieval
   - Top-k relevant passages
   - Source citations
   - Snippet previews

5. **Interaction Logs** - Logging interface
   - JSONL log entries
   - Prompt documentation
   - Timestamp tracking

### Demo Video

A short demo video (3-5 minutes) will be added here showing:

- Complete workflow from assignment input to deliverables
- Plan editing and re-execution
- Generated file outputs
- System design walkthrough

## File Naming Convention

- `screenshot1_ui_overview.png`
- `screenshot2_plan_generation.png`
- `screenshot3_task_execution.png`
- `screenshot4_rag_integration.png`
- `screenshot5_interaction_logs.png`
- `demo_video.mp4` or `demo_video_link.txt`

## Recording Tools Used

- **Screenshots:** macOS Screenshot (Cmd+Shift+4) / Windows Snipping Tool / Linux GNOME Screenshot
- **Screen Recording:** OBS Studio / SimpleScreenRecorder / macOS QuickTime
- **Video Editing (optional):** DaVinci Resolve / iMovie / Kdenlive

## Demo Script

### 3-Minute Demo Flow

**0:00-0:15** - Introduction
- Brief project overview
- Problem statement

**0:15-0:45** - Architecture
- Show system_design.md diagram
- Explain Planner → Executor flow

**0:45-1:45** - Live Demo (60s)
- Paste assignment description
- Click "Plan & Generate"
- Show JSON plan output
- Edit plan (optional)
- Click "Run first task"
- Show generated README.md
- Show generated Java skeleton (if implemented)

**1:45-2:15** - Interaction Logs (30s)
- Open interactions.jsonl
- Show logged prompts and responses
- Open prompts_used.md

**2:15-2:45** - RAG Demo (30s, if implemented)
- Show resource retrieval
- Display citations

**2:45-3:00** - Closing (15s)
- Recap key features
- Future enhancements
- Contact information

## Notes

- Screenshots should be high-resolution (1920x1080 or higher)
- Demo video should include voiceover or captions
- Ensure all sensitive information (API keys, personal data) is redacted
- Compress video files to keep repository size manageable

---

**To add screenshots/videos:**

```bash
# From repository root
cd demo/

# Add screenshots
cp ~/path/to/screenshot1.png .

# Add video (or just a link to YouTube/Drive)
echo "Demo Video: https://youtu.be/YOUR_VIDEO_ID" > demo_video_link.txt

# Commit
git add .
git commit -m "Add demo screenshots and video"
git push
```

---

**Last Updated:** November 03, 2025  
**Author:** Aditya Deshmukh (adityad23@iitk.ac.in)
