# AI Business Automation Pipeline 🤖🚀

> A modular, production-ready multi-agent AI system that automates business workflows — from lead intake to reply generation to strategic decision-making.

---

## ✨ Features

- 🔍 **Lead Analysis Agent** — classifies intent, priority, and category from any message
- ✉️ **Reply Generation Agent** — generates personalized, professional email replies
- 📊 **Strategy Agent** — recommends the next best business action
- 🔗 **Chained Pipeline** — all three agents work sequentially, each building on the last
- 💾 **JSON Output** — structured results saved automatically for every run
- ⚡ **Zero dependencies** — runs out of the box with pure Python
- 🔌 **API-ready** — plug in Claude or OpenAI with a single flag

---

## 🧠 System Architecture

```
Lead Input
    │
    ▼
┌──────────────────────┐
│  Lead Analysis Agent  │  ── Detects intent, priority, keywords
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Reply Generation Agent│  ── Writes a personalized professional reply
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│    Strategy Agent     │  ── Decides the best next action + timeline
└──────────┬───────────┘
           │
           ▼
  Structured JSON Output
```

---

## 🔄 How Each Agent Works

### 🔍 Lead Analysis Agent (`agents/analysis_agent.py`)
Receives the raw lead message and returns structured metadata:
- **Intent** — Business Inquiry, Partnership, Support Request, Sales/Demo, Information Request
- **Priority** — High / Medium / Low (based on urgency keywords)
- **Category** — Sales, Business Development, Customer Support, Marketing
- **Keywords** — key topics extracted from the message
- **Summary** — one-line overview

### ✉️ Reply Generation Agent (`agents/reply_agent.py`)
Uses the lead + analysis to generate a tailored email reply:
- Selects the right tone and structure based on intent
- Personalized to the lead's specific need
- Professional and ready to send

### 📊 Strategy Agent (`agents/strategy_agent.py`)
Recommends the next action based on intent + priority:
- Specific action (e.g., "Book Discovery Call", "Escalate Immediately")
- Clear rationale and timeline
- Follow-up day count

---

## 🛠 Tech Stack

| Component       | Details                              |
|----------------|--------------------------------------|
| Language        | Python 3.10+                        |
| Mode (default)  | Simulated — no API key required     |
| Mode (optional) | Claude API (`anthropic` library)    |
| Dependencies    | None for simulated mode             |
| Output          | Terminal + `output/results.json`    |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/pratiksangle01/ai-business-automation-pipeline.git
cd ai-business-automation-pipeline
```

### 2. Run the pipeline (no setup needed)

```bash
python pipeline.py
```

> ✅ Works immediately — no API key, no installs, no configuration.

### 3. (Optional) Enable real AI API mode

Install the Anthropic SDK:

```bash
pip install anthropic
```

Set your API key:

```bash
# macOS / Linux
export ANTHROPIC_API_KEY="your_api_key_here"

# Windows
setx ANTHROPIC_API_KEY "your_api_key_here"
```

Then change `use_api=False` to `use_api=True` in `pipeline.py`:

```python
results = run_pipeline(sample_leads, use_api=True)
```

---

## 📌 Example

**Input leads (`pipeline.py`):**
```python
sample_leads = [
    "Hi, I'm looking to build a website for my e-commerce store. Can you help?",
    "I'm having trouble logging into my account. Please assist ASAP.",
    "We'd love to schedule a demo call to learn more about your services.",
]
```

**Terminal output:**
```
=================================================================
   AI BUSINESS AUTOMATION PIPELINE
=================================================================
  Processing 3 lead(s)  |  2025-03-20 10:00:00
=================================================================

📥 Lead 1/3
   Hi, I'm looking to build a website for my e-commerce store...
-----------------------------------------------------------------
🔍 [Analysis Agent]   Running...
✉️  [Reply Agent]      Generating reply...
📊 [Strategy Agent]   Deciding next step...

  ─────────────────────────────────────────────────────────────
  📋 LEAD 1 RESULTS
  ─────────────────────────────────────────────────────────────
  📥 Lead      : Hi, I'm looking to build a website for my e-commerce...
  🎯 Intent    : Business Inquiry
  🟡 Priority  : Medium
  🏷️  Category  : Sales
  🔑 Keywords  : website, build, help
  📝 Summary   : Lead identified as a 'Business Inquiry' with Medium priority.

  📊 STRATEGY
  ─────────────────────────────────────────────────────────────
  ✅ Action    : Send Portfolio
  💡 Rationale : Share portfolio and case studies, then follow up in 2 days.
  ⏰ Timeline  : Within 1–3 business days
  📅 Follow Up : In 3 day(s)

  ✉️  GENERATED REPLY (preview)
  ─────────────────────────────────────────────────────────────
  Hi,

  Thank you for reaching out! I'd be happy to help you with your project.
  ...
```

**JSON output (`output/results.json`):**
```json
{
  "lead_id": 1,
  "lead": "Hi, I'm looking to build a website...",
  "analysis": {
    "intent": "Business Inquiry",
    "priority": "Medium",
    "category": "Sales",
    "keywords": ["website", "build", "help"],
    "summary": "Lead identified as a 'Business Inquiry' with Medium priority."
  },
  "generated_reply": "Hi,\n\nThank you for reaching out!...",
  "suggested_action": {
    "action": "Send Portfolio",
    "rationale": "Share portfolio and case studies, then follow up in 2 days.",
    "timeline": "Within 1–3 business days",
    "follow_up_days": 3
  }
}
```

---

## 📁 Project Structure

```
ai-business-automation-pipeline/
│
├── pipeline.py                  # Main entry point — runs the full pipeline
│
├── agents/
│   ├── __init__.py
│   ├── analysis_agent.py        # Lead Analysis Agent
│   ├── reply_agent.py           # Reply Generation Agent
│   └── strategy_agent.py       # Strategy Agent
│
├── utils/
│   ├── __init__.py
│   └── logger.py                # Structured terminal output
│
├── output/
│   ├── results.json             # Auto-generated on each run
│   └── example_results.json     # Sample output for reference
│
├── requirements.txt
└── README.md
```

---

## 🔮 Roadmap

- [ ] Claude / OpenAI API integration (simulated mode already built-in)
- [ ] Gmail automation — send generated replies directly
- [ ] CSV import — load leads from a spreadsheet
- [ ] Web dashboard (Flask / Streamlit UI)
- [ ] Parallel agent execution for faster processing
- [ ] Memory-based agents with session history
- [ ] CRM integration (HubSpot, Notion, Airtable)

---

## 💼 Use Cases

- Freelancers automating client inquiry handling
- Agencies managing high volumes of inbound leads
- Sales teams building automated follow-up workflows
- Developers prototyping multi-agent AI systems
- Startups building AI-powered customer communication

---

## 👨‍💻 Author

**Pratik Sangle**  
Feel free to connect, open an issue, or contribute!

---

⭐ If this project helped you, consider giving it a star — it means a lot!
