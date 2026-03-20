"""
Strategy Agent
==============
Recommends the next best action for a lead based on:
  - Intent classification
  - Priority level
  - Lead content

Runs in two modes:
  - Simulated (default): logic-based decisions, no API key needed
  - API mode: calls Claude/OpenAI for contextual strategy suggestions
"""


# ── Action rules: (intent, priority) → action ──────────────────────────────────
ACTION_RULES = {
    ("Business Inquiry",    "High"):   ("Book Discovery Call",   "Schedule a call within 24 hours. High-value prospect."),
    ("Business Inquiry",    "Medium"): ("Send Portfolio",        "Share portfolio and case studies, then follow up in 2 days."),
    ("Business Inquiry",    "Low"):    ("Send Info Package",     "Send service overview email and wait for response."),
    ("Partnership",         "High"):   ("Schedule Partnership Call", "Arrange a call within 48 hours. Strong alignment signal."),
    ("Partnership",         "Medium"): ("Send Partnership Deck", "Share partnership proposal and follow up in 3 days."),
    ("Partnership",         "Low"):    ("Add to Nurture List",   "Add to newsletter and long-term nurture sequence."),
    ("Support Request",     "High"):   ("Escalate Immediately",  "Resolve within 2 hours. Flag to support team now."),
    ("Support Request",     "Medium"): ("Respond Same Day",      "Acknowledge and resolve within the same business day."),
    ("Support Request",     "Low"):    ("Standard Support Flow", "Add to support queue and respond within 24 hours."),
    ("Sales / Demo",        "High"):   ("Book Demo Call",        "Confirm demo slot immediately while interest is hot."),
    ("Sales / Demo",        "Medium"): ("Send Demo Booking Link","Share booking link and follow up in 24 hours."),
    ("Sales / Demo",        "Low"):    ("Send Demo Video",       "Share a recorded walkthrough to warm them up."),
    ("Information Request", "High"):   ("Send Info + Follow Up", "Send detailed info pack and follow up within 24 hours."),
    ("Information Request", "Medium"): ("Send Info Package",     "Send service brochure and pricing. Follow up in 3 days."),
    ("Information Request", "Low"):    ("Add to Email List",     "Add to marketing list for automated nurture sequence."),
    ("General Inquiry",     "High"):   ("Qualify Immediately",   "Reach out to clarify needs and qualify the lead."),
    ("General Inquiry",     "Medium"): ("Send Introduction",     "Reply with a short company intro and ask qualifying questions."),
    ("General Inquiry",     "Low"):    ("Monitor",               "Log the lead and follow up in a week if no response."),
}

TIMELINE_MAP = {
    "High":   "Within 2–24 hours",
    "Medium": "Within 1–3 business days",
    "Low":    "Within 1 week",
}


class StrategyAgent:
    """
    Suggests the next best action for a lead based on intent and priority.
    """

    def __init__(self, use_api: bool = False):
        self.use_api = use_api

    def suggest(self, lead: str, analysis: dict) -> dict:
        """
        Suggest next action for the lead.

        Args:
            lead:     Raw lead message
            analysis: Structured dict from LeadAnalysisAgent

        Returns:
            dict with action, rationale, timeline, follow_up_days
        """
        if self.use_api:
            return self._suggest_with_api(lead, analysis)
        return self._suggest_simulated(lead, analysis)

    # ── Simulated (rule-based) ──────────────────────────────────────────────────

    def _suggest_simulated(self, lead: str, analysis: dict) -> dict:
        intent   = analysis.get("intent",   "General Inquiry")
        priority = analysis.get("priority", "Medium")

        key = (intent, priority)
        action, rationale = ACTION_RULES.get(
            key,
            ("Follow Up", "Review manually and decide on next steps.")
        )

        return {
            "action":       action,
            "rationale":    rationale,
            "timeline":     TIMELINE_MAP.get(priority, "Within 3 days"),
            "follow_up_days": {"High": 1, "Medium": 3, "Low": 7}.get(priority, 3),
        }

    # ── API mode ────────────────────────────────────────────────────────────────

    def _suggest_with_api(self, lead: str, analysis: dict) -> dict:
        """
        Use Claude API for contextual, intelligent strategy recommendations.
        Requires ANTHROPIC_API_KEY environment variable.
        """
        try:
            import anthropic, json, re, os
            client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

            prompt = (
                f"You are a business strategy advisor.\n\n"
                f"Lead message: \"{lead}\"\n\n"
                f"Analysis:\n"
                f"  - Intent: {analysis.get('intent')}\n"
                f"  - Priority: {analysis.get('priority')}\n"
                f"  - Keywords: {', '.join(analysis.get('keywords', []))}\n\n"
                f"Recommend the next best business action. "
                f"Return ONLY a JSON object with these exact keys:\n"
                f'{{"action": "...", "rationale": "...", "timeline": "...", "follow_up_days": <number>}}'
            )

            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=250,
                messages=[{"role": "user", "content": prompt}]
            )
            text = response.content[0].text.strip()
            text = re.sub(r"```json|```", "", text).strip()
            return json.loads(text)

        except Exception as e:
            print(f"   ⚠️  API error ({e}), falling back to simulated mode.")
            return self._suggest_simulated(lead, analysis)
