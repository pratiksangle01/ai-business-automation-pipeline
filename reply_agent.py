"""
Reply Generation Agent
======================
Generates a personalized, professional email reply based on:
  - The original lead message
  - The structured analysis from LeadAnalysisAgent

Runs in two modes:
  - Simulated (default): template-based generation, no API key needed
  - API mode: calls Claude/OpenAI for fully custom replies
"""


# ── Reply templates per intent ──────────────────────────────────────────────────
REPLY_TEMPLATES = {
    "Business Inquiry": (
        "Hi,\n\n"
        "Thank you for reaching out! I'd be happy to help you with your project.\n\n"
        "Based on your message, I understand you're looking for {intent_detail}. "
        "I'd love to learn more about your requirements so I can suggest the best solution.\n\n"
        "Could we schedule a quick call this week to discuss the details?\n\n"
        "Looking forward to hearing from you.\n\n"
        "Best regards,\nPratik Sangle"
    ),
    "Partnership": (
        "Hi,\n\n"
        "Thank you for considering a partnership — I'm excited to explore this opportunity!\n\n"
        "Long-term collaborations are something I genuinely value, and I believe we could "
        "create real value together. I'd love to understand more about your goals and how "
        "we can align our efforts.\n\n"
        "Let's schedule a discovery call at your convenience. Please share your availability "
        "and I'll confirm a time that works.\n\n"
        "Warm regards,\nPratik Sangle"
    ),
    "Support Request": (
        "Hi,\n\n"
        "I'm sorry to hear you're experiencing an issue — I completely understand how "
        "frustrating that can be, and I want to resolve this for you as quickly as possible.\n\n"
        "To assist you efficiently, could you please share:\n"
        "  1. A brief description of the issue\n"
        "  2. Any error messages you're seeing\n"
        "  3. The steps you took before the issue occurred\n\n"
        "I'll prioritize this and get back to you with a solution shortly.\n\n"
        "Best regards,\nPratik Sangle"
    ),
    "Sales / Demo": (
        "Hi,\n\n"
        "Thank you for your interest — I'd love to walk you through everything!\n\n"
        "I can arrange a personalized demo that covers exactly what you're looking for. "
        "It typically takes 20–30 minutes and you'll come away with a clear picture of "
        "how this can help your business.\n\n"
        "Please let me know your preferred time, or feel free to book directly using "
        "the link below:\n"
        "📅 [Insert Calendly / Booking Link]\n\n"
        "Looking forward to connecting!\n\n"
        "Best regards,\nPratik Sangle"
    ),
    "Information Request": (
        "Hi,\n\n"
        "Thank you for your message! I'm happy to share more details.\n\n"
        "I've attached our service overview and pricing guide for your reference. "
        "Here's a quick summary:\n"
        "  • Full-stack web & app development\n"
        "  • AI automation solutions\n"
        "  • Ongoing support & maintenance\n\n"
        "If you have specific questions after reviewing, please don't hesitate to ask. "
        "I'm also happy to jump on a quick call if that's easier.\n\n"
        "Best regards,\nPratik Sangle"
    ),
    "General Inquiry": (
        "Hi,\n\n"
        "Thank you for getting in touch!\n\n"
        "I'd love to understand your needs better so I can point you in the right direction. "
        "Could you share a bit more about what you're looking for?\n\n"
        "I'm here to help and will respond promptly.\n\n"
        "Best regards,\nPratik Sangle"
    ),
}

INTENT_DETAIL_MAP = {
    "Business Inquiry":    "professional services or a development project",
    "Partnership":         "a business partnership or collaboration",
    "Support Request":     "support with an existing issue",
    "Sales / Demo":        "a product demo or walkthrough",
    "Information Request": "details about services or pricing",
    "General Inquiry":     "more information",
}


class ReplyGenerationAgent:
    """
    Generates a professional email reply for a given lead and its analysis.
    """

    def __init__(self, use_api: bool = False):
        self.use_api = use_api

    def generate(self, lead: str, analysis: dict) -> str:
        """
        Generate a reply based on lead content and analysis.

        Args:
            lead:     Raw lead message
            analysis: Structured dict from LeadAnalysisAgent

        Returns:
            Formatted email reply string
        """
        if self.use_api:
            return self._generate_with_api(lead, analysis)
        return self._generate_simulated(lead, analysis)

    # ── Simulated (template-based) ──────────────────────────────────────────────

    def _generate_simulated(self, lead: str, analysis: dict) -> str:
        intent = analysis.get("intent", "General Inquiry")
        template = REPLY_TEMPLATES.get(intent, REPLY_TEMPLATES["General Inquiry"])
        intent_detail = INTENT_DETAIL_MAP.get(intent, "your needs")
        return template.format(intent_detail=intent_detail)

    # ── API mode ────────────────────────────────────────────────────────────────

    def _generate_with_api(self, lead: str, analysis: dict) -> str:
        """
        Use Claude API to generate a custom, contextual reply.
        Requires ANTHROPIC_API_KEY environment variable.
        """
        try:
            import anthropic, os
            client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

            prompt = (
                f"You are a professional business assistant.\n\n"
                f"A lead has sent the following message:\n\"{lead}\"\n\n"
                f"Analysis:\n"
                f"  - Intent: {analysis.get('intent')}\n"
                f"  - Priority: {analysis.get('priority')}\n"
                f"  - Keywords: {', '.join(analysis.get('keywords', []))}\n\n"
                f"Write a professional, warm, and concise email reply. "
                f"Sign off as 'Pratik Sangle'. Return only the email body, no subject line."
            )

            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=400,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()

        except Exception as e:
            print(f"   ⚠️  API error ({e}), falling back to simulated mode.")
            return self._generate_simulated(lead, analysis)
