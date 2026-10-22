# RecallOS — The AI That Knows What You're About to Forget

A runnable **Alexa+-style simulated experience** for the Build, Ship, Shape Amazon Developer Hackathon.

## What is real
- SQLite-persisted student memory state and quiz history
- Decay-based retention estimates and explainable risk ranking
- Dependency/knowledge graph data for concepts
- Adaptive review: quiz performance changes stability and next-review timing
- Backend agent tool routing: forecast, rescue quiz, revision plan, explanation
- Browser voice input (where supported), chat, dashboard and action traces

## Limitations (important for your submission)
This is a **simulated Alexa+ experience**, not a deployed Alexa+ add-on and not a real Alexa device integration. The agent is a transparent, deterministic tool-routing agent, **not an LLM**. Memory-retention estimates are illustrative, **not validated individual predictions**. The initial topics and scores are demo data. Browser voice recognition requires a compatible browser and may use that browser's online speech service. No third-party key is required to run this project.

## Run on Windows (VS Code / PowerShell)
1. Extract the ZIP and open the `RecallOS` folder in VS Code.
2. Make sure Python 3.10+ is installed: `python --version`.
3. Open Terminal > New Terminal in the project folder.
4. Run `python app.py`.
5. Visit **http://localhost:8000** in Chrome/Edge.
6. Try *Voice agent > What am I about to forget?* then *Quiz me*.

If `python` is not recognized, try `py app.py`.

## Test
`python -m unittest discover -s tests -v`

## Agent architecture
`Web UI / voice transcript → /api/agent → intent router → forecast/plan/quiz selector → SQLite`
`Web UI → /api/answer → correct-answer evaluation → memory-stability update → SQLite → refreshed dashboard`

The simulation is eligible as an Alexa+ alternative route according to the official rules, but judges assess functionality and completeness; eligibility is ultimately determined by the organizer. Official rules: https://amazonappdev2026.devpost.com/rules

## Suggested demo recording (<3 min)
1. Show dashboard with risk-ranked concepts.
2. Go to Agent and ask “What am I about to forget?”; highlight the tool trace.
3. Ask “Quiz me”, complete the question and show the updated retention.
4. Ask for your study plan.
5. Clearly state this is an Alexa+-style **web simulation**, with no physical Alexa integration.

## Recommended next features
- Replace deterministic intent router with LLM/agent SDK with actual tool calls.
- Enable student note upload and concept extraction.
- Add calendar scheduling and notifications with user permission.
- Add more rigorous evaluation of recall and spaced repetition algorithms.

## Tech stack
Python standard-library HTTP server, SQLite, HTML/CSS/vanilla JavaScript. No installs, subscriptions, API keys, or accounts required for the demo.

## License
MIT — see LICENSE.


## New in v2: Import your own notes

Open **My study notes** and paste definitions, one per line:

```text
Backpropagation: An algorithm for computing neural-network gradients using the chain rule.
Regularization: Techniques that reduce model complexity to improve generalization.
```

Choose **Import concepts**. New cards appear in the forgetting forecast, quizzes, and priority planner. During each imported card's quiz, choose **Reveal reference definition** before honestly self-rating your recollection. The imported text and attempts remain stored in local SQLite. Max 15 new cards per import, up to 12,000 characters. Existing concept names are skipped.

This feature uses deterministic parsing; it does not generate LLM questions, provide automatic free-text grading, or connect to a real Alexa+ service. Those are future enhancements.


## New in V3 — Optional LLM-powered tool calling

The agent can now select one of four server-side tools using an OpenAI-compatible chat-completions API: `get_memory_risk`, `start_memory_rescue`, `build_revision_plan`, or `explain_memory_priority`. The server executes the selected operation on real SQLite data, and the dashboard displays its tool trace. No API credentials are put into client-side JavaScript.

**Enable on Windows PowerShell** (only if you have a compatible API key):

```powershell
$env:RECALLOS_API_KEY = "your-api-key-here"
$env:RECALLOS_MODEL = "gpt-4o-mini"
python app.py
```

For another OpenAI-compatible provider, set `$env:RECALLOS_API_BASE = "https://provider.example/v1"` and the provider's correct model ID. Tool calling support is required; not all models/providers implement it. The app defaults to `https://api.openai.com/v1` and `gpt-4o-mini` when only a key is set. **Do not commit real API keys to GitHub.** If you don't have a key, `python app.py` works exactly as before with deterministic offline routing. If the remote call fails, RecallOS falls back to the offline agent. API calls may cost money, depending on your provider.

**Check agent status:** open `http://localhost:8000/api/health`; the `agent_mode` will say `llm-enabled` if the key is present (this alone does not guarantee the provider is reachable). In the dashboard's Voice Agent screen, the action trace shows `llm-tool-call` only when an actual model-selected tool was executed.

**Privacy:** With an API key enabled, the user's chat message and a summary of saved topic names and memory scores are sent to the configured API provider. Full pasted notes are not included in this request. Without an API key, notes and messages stay with the local backend (browser speech recognition can still be network-based).

**Scope:** This is still a simulated Alexa+ web experience, not an official Alexa+ endpoint or deployment. The LLM selects a tool but does not independently verify users' answers or invent memory predictions. Existing quizzes, note imports, and memory model remain intact.
