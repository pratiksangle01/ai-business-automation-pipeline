"""
Lead Analysis Agent
===================
Analyzes incoming lead messages to identify:
  - Intent  (what does the lead want?)
  - Priority (how urgently should we respond?)
  - Category (what type of lead is this?)
  - Keywords (key topics detected)

Runs in two modes:
  - Simulated (default): rule-based logic, no API key needed
  - API mode: calls Claude/OpenAI for richer analysis
"""

import re


# ── Intent classification rules ────────────────────────────────────────────────
INTENT_RULES = {
    "Business Inquiry": [
        "website", "app", "build", "develop", "project", "service",
        "pricing", "cost", "quote", "hire", "help", "portfolio"
    ],
    "Partnership": [
        "partner", "partnership", "collaborate", "collaboration",
        "outsource", "long-term", "contract", "joint", "agency"
    ],
    "Support Request": [
        "issue", "problem", "error", "bug", "trouble", "not working",
        "help", "fix", "broken", "login", "account", "urgent", "asap"
    ],
    "Sales / Demo": [
        "demo", "trial", "schedule", "call", "meeting", "presentation",
        "interested", "learn more", "show", "walkthrough"
    ],
    "Information Request": [
        "details", "information", "info", "how does", "what is",
        "explain", "brochure", "send me", "plan", "feature"
    ],
}

PRIORITY_KEYWORDS = {
    "High":   ["urgent", "asap", "immediately", "critical", "emergency", "today"],
    "Medium": ["interested", "looking", "would like", "schedule", "meeting"],
    "Low":    ["just curious", "sometime", "maybe", "considering", "general"],
}


class LeadAnalysisAgent:
    """
    Analyzes a raw lead message and returns a structured analysis dict.
    """

    def __init__(self, use_api: bool = False):
        self.use_api = use_api

    def analyze(self, lead: str) -> dict:
        """
        Analyze a lead and return structured data.

        Args:
            lead: Raw lead message string

        Returns:
            dict with intent, priority, category, keywords, summary
        """
        if self.use_api:
            return self._analyze_with_api(lead)
        return self._analyze_simulated(lead)

    # ── Simulated (rule-based) ──────────────────────────────────────────────────

    def _analyze_simulated(self, lead: str) -> dict:
        lead_lower = lead.lower()

        intent   = self._classify_intent(lead_lower)
        priority = self._classify_priority(lead_lower)
        keywords = self._extract_keywords(lead_lower)
        summary  = self._generate_summary(lead, intent, priority)

        return {
            "intent":   intent,
            "priority": priority,
            "category": self._map_category(intent),
            "keywords": keywords,
            "summary":  summary,
        }

    def _classify_intent(self, lead_lower: str) -> str:
        scores = {}
        for intent, keywords in INTENT_RULES.items():
            scores[intent] = sum(1 for kw in keywords if kw in lead_lower)
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else "General Inquiry"

    def _classify_priority(self, lead_lower: str) -> str:
        for priority, keywords in PRIORITY_KEYWORDS.items():
            if any(kw in lead_lower for kw in keywords):
                return priority
        return "Medium"

    def _extract_keywords(self, lead_lower: str) -> list[str]:
        all_keywords = [kw for kws in INTENT_RULES.values() for kw in kws]
        found = [kw for kw in all_keywords if kw in lead_lower]
        return list(dict.fromkeys(found))[:6]  # deduplicate, max 6

    def _generate_summary(self, lead: str, intent: str, priority: str) -> str:
        return (
            f"Lead identified as a '{intent}' with {priority} priority. "
            f"Message is {len(lead.split())} words long."
        )

    def _map_category(self, intent: str) -> str:
        mapping = {
            "Business Inquiry":    "Sales",
            "Partnership":         "Business Development",
            "Support Request":     "Customer Support",
            "Sales / Demo":        "Sales",
            "Information Request": "Marketing",
            "General Inquiry":     "General",
        }
        return mapping.get(intent, "General")

    # ── API mode ────────────────────────────────────────────────────────────────

    def _analyze_with_api(self, lead: str) -> dict:
        """
        Use Claude API for richer analysis.
        Requires ANTHROPIC_API_KEY environment variable.
        """
        try:
            import anthropic, json, os
            client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

            prompt = f"""Analyze this business lead message and return ONLY a JSON object.

Lead: "{lead}"

Return this exact structure:
{{
  "intent": "<one of: Business Inquiry | Partnership | Support Request | Sales / Demo | Information Request | General Inquiry>",
  "priority": "<one of: High | Medium | Low>",
  "category": "<one of: Sales | Business Development | Customer Support | Marketing | General>",
  "keywords": ["keyword1", "keyword2"],
  "summary": "<one sentence summary>"
}}"""

            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            text = response.content[0].text.strip()
            text = re.sub(r"```json|```", "", text).strip()
            return json.loads(text)

        except Exception as e:
            print(f"   ⚠️  API error ({e}), falling back to simulated mode.")
            return self._analyze_simulated(lead)
