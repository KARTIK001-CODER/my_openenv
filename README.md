---
title: Meeting Intelligence Env
emoji: 📈
colorFrom: red
colorTo: red
sdk: docker
pinned: false
---

# 🧠 AI Meeting Decision Intelligence Environment

**Standardizing the Evaluation of Executive-Level AI Agents**

---

## 1. PROJECT OVERVIEW
Modern Large Language Models (LLMs) often excel at chat but struggle to extract **structured, prioritized decisions** from noisy, real-world professional transcripts. 

The **AI Meeting Decision Intelligence Environment** is a standardized OpenEnv benchmark that simulates business-critical tasks found in productivity tools like Slack, Zoom, and Notion. It challenges AI agents to process raw meeting data and synthesize it into actionable intelligence.

## 2. WHY THIS MATTERS
"Decision Intelligence" is the bridge between raw data and business outcomes. This environment benchmarks an agent's ability to:
- **Filter Noise**: Distinguish between casual banter and critical directives.
- **Prioritize**: Dynamically assign urgency to tasks based on conversational context.
- **Synthesize**: Move beyond simple list extraction to high-level executive summarization.

By measuring these specific capabilities, we can evaluate the reliability of LLM agents in production corporate environments.

## 3. CORE ARCHITECTURE
- **Environment**: Manages the state and provides a Gymnasium-style interface (`reset`/`step`).
- **Tasks**: A collection of high-fidelity meeting transcripts ranging from simple sync-ups to high-noise strategy sessions.
- **Grader**: A deterministic scoring engine that computes the **Intel Score** based on extraction accuracy and rigor.
- **Inference Pipeline**: A fail-safe loop that processes agent output through robust JSON extraction.

## 4. OBSERVATION SPACE
The environment provides the following state to the agent:
```json
{
  "meeting_notes": "Raw transcript text with timestamps and noise...",
  "current_summary": "Empty or previously submitted summary.",
  "action_items": [],
  "feedback": "Grading logic feedback from past steps."
}
```

## 5. ACTION SPACE
The agent must submit intelligence in the following structured format:
```json
{
  "summary": "Deep executive summary of the Strategic Pivot...",
  "action_items": [
    {
      "task": "Migrate API cluster to AWS Frankfurt",
      "priority": "High"
    },
    {
      "task": "Review security logs for 2024",
      "priority": "Medium"
    }
  ]
}
```
*Valid priorities: `High`, `Medium`, `Low`.*

## 6. REWARD DESIGN
The **Intel Score** is computed deterministically on a scale of **0.0 to 1.0**:
- **Summary Depth (30%)**: Rewards professional-grade summarization (>100 characters).
- **Extraction Accuracy (40%)**: Reward based on identifying the correct number of distinct directives.
- **Metadata Integrity (30%)**: Penalizes vague task descriptions or missing/invalid priority levels.

## 7. TASK DESIGN
1.  **EASY (Sync-up)**: A clean, 2-speaker call with a single, explicit action.
2.  **MEDIUM (Project Alpha)**: Multi-speaker technical update featuring overlapping tasks and 3 distinct objectives.
3.  **HARD (Strategic Strategy)**: High-noise session with crosstalk, interruptions, and irrelevant "water-cooler" talk. Requires filtering out noise from 4+ complex action items.

## 8. INTEL SCORE (DECISION INTELLIGENCE SCORE)
The final result of an evaluation is the **Intel Score**:
- **0.0 - 0.3 (Foundational)**: Agent likely struggled with the JSON format or provided vague, short summaries.
- **0.4 - 0.7 (Functional)**: Agent extracted most tasks but missed priority nuances or provided basic summaries.
- **0.8 - 1.0 (Advanced)**: Agent navigated heavy noise, prioritized correctly, and provided executive-level depth.

## 9. DETERMINISM STATEMENT
This environment is **100% deterministic**.
- All tasks are predefined and static.
- The grading logic uses strict thresholds (length, count, enums).
- The same input from an agent will always produce the exact same Intel Score.

## 10. OPENENV COMPLIANCE
This project is strictly compliant with the OpenEnv core specification:
- Implements `step()`, `reset()`, and `state()` methods.
- Includes a valid `openenv.yaml` manifest.
- Successfully passes all `openenv-core` validation checks.

## 11. SETUP & RUN
Follow these commands to run a local evaluation:

**Windows PowerShell:**
```powershell
# Set environmental variables
$env:HF_TOKEN = "your_actual_token_here"
$env:MODEL_NAME = "meta-llama/Meta-Llama-3.1-8B-Instruct"
$env:API_BASE_URL = "https://router.huggingface.co/v1" # Verified Router Endpoint

# Run the inference evaluation
python inference.py
```

## 12. DEPLOYMENT
- **Docker Support**: Build the image with `docker build -t meeting-intel .`.
- **Hugging Face Spaces**: Compatible with HF Spaces for community-wide benchmarking and hosting.

---
*Developed for OpenEnv Hackathon 2024.*
