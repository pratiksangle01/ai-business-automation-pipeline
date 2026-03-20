"""
AI Business Automation Pipeline
================================
Chains three agents together to process leads end-to-end:
  Lead Analysis Agent → Reply Generation Agent → Strategy Agent
"""

import json
from datetime import datetime
from agents.analysis_agent import LeadAnalysisAgent
from agents.reply_agent import ReplyGenerationAgent
from agents.strategy_agent import StrategyAgent
from utils.logger import log_result


def run_pipeline(leads: list[str], use_api: bool = False) -> list[dict]:
    """
    Run the full automation pipeline on a list of leads.

    Args:
        leads: List of raw lead messages or emails
        use_api: If True, uses real Claude/OpenAI API (requires API key setup)

    Returns:
        List of structured results for each lead
    """
    analysis_agent  = LeadAnalysisAgent(use_api=use_api)
    reply_agent     = ReplyGenerationAgent(use_api=use_api)
    strategy_agent  = StrategyAgent(use_api=use_api)

    results = []

    print("\n" + "=" * 65)
    print("   AI BUSINESS AUTOMATION PIPELINE")
    print("=" * 65)
    print(f"  Processing {len(leads)} lead(s)  |  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)

    for i, lead in enumerate(leads, 1):
        print(f"\n📥 Lead {i}/{len(leads)}")
        print(f"   {lead[:80]}{'...' if len(lead) > 80 else ''}")
        print("-" * 65)

        # Stage 1 — Analysis
        print("🔍 [Analysis Agent]   Running...")
        analysis = analysis_agent.analyze(lead)

        # Stage 2 — Reply
        print("✉️  [Reply Agent]      Generating reply...")
        reply = reply_agent.generate(lead, analysis)

        # Stage 3 — Strategy
        print("📊 [Strategy Agent]   Deciding next step...")
        strategy = strategy_agent.suggest(lead, analysis)

        result = {
            "lead_id":        i,
            "lead":           lead,
            "analysis":       analysis,
            "generated_reply": reply,
            "suggested_action": strategy,
            "timestamp":      datetime.now().isoformat()
        }

        results.append(result)
        log_result(result)

        print(f"\n✅ Lead {i} complete.")

    print("\n" + "=" * 65)
    print(f"  Pipeline complete. {len(results)} lead(s) processed.")
    print("=" * 65 + "\n")

    return results


def save_results(results: list[dict], filepath: str = "output/results.json"):
    """Save pipeline results to a JSON file."""
    import os
    os.makedirs("output", exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(results, f, indent=2)
    print(f"💾 Results saved to {filepath}")


if __name__ == "__main__":
    # ── Sample leads ──────────────────────────────────────────────
    sample_leads = [
        "Hi, I'm looking to build a website for my e-commerce store. Can you help?",
        "We are interested in a long-term partnership for outsourcing our IT support.",
        "I'm having trouble logging into my account. Please assist ASAP.",
        "Can you send me your pricing and service details?",
        "We'd love to schedule a demo call to learn more about your services.",
    ]

    results = run_pipeline(sample_leads, use_api=False)
    save_results(results)

    # ── Pretty print summary ───────────────────────────────────────
    print("\n📋 FULL RESULTS SUMMARY")
    print("=" * 65)
    for r in results:
        print(f"\n🔹 Lead {r['lead_id']}: {r['lead'][:60]}...")
        print(f"   Intent:  {r['analysis']['intent']}")
        print(f"   Priority:{r['analysis']['priority']}")
        print(f"   Action:  {r['suggested_action']['action']}")
        print(f"   Reply:   {r['generated_reply'][:100]}...")
