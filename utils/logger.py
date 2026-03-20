"""
Logger Utility
==============
Handles structured terminal output for each processed lead.
"""


PRIORITY_COLORS = {
    "High":   "🔴",
    "Medium": "🟡",
    "Low":    "🟢",
}


def log_result(result: dict):
    """Print a clean, structured summary of a processed lead."""
    analysis = result.get("analysis", {})
    strategy = result.get("suggested_action", {})
    reply    = result.get("generated_reply", "")

    priority_icon = PRIORITY_COLORS.get(analysis.get("priority", "Medium"), "🟡")

    print(f"\n  {'─'*59}")
    print(f"  📋 LEAD {result['lead_id']} RESULTS")
    print(f"  {'─'*59}")
    print(f"  📥 Lead      : {result['lead'][:70]}{'...' if len(result['lead']) > 70 else ''}")
    print(f"  🎯 Intent    : {analysis.get('intent', 'N/A')}")
    print(f"  {priority_icon} Priority  : {analysis.get('priority', 'N/A')}")
    print(f"  🏷️  Category  : {analysis.get('category', 'N/A')}")
    print(f"  🔑 Keywords  : {', '.join(analysis.get('keywords', []))}")
    print(f"  📝 Summary   : {analysis.get('summary', 'N/A')}")
    print(f"\n  📊 STRATEGY")
    print(f"  {'─'*59}")
    print(f"  ✅ Action    : {strategy.get('action', 'N/A')}")
    print(f"  💡 Rationale : {strategy.get('rationale', 'N/A')}")
    print(f"  ⏰ Timeline  : {strategy.get('timeline', 'N/A')}")
    print(f"  📅 Follow Up : In {strategy.get('follow_up_days', 'N/A')} day(s)")
    print(f"\n  ✉️  GENERATED REPLY (preview)")
    print(f"  {'─'*59}")
    for line in reply.split("\n")[:6]:
        print(f"  {line}")
    print(f"  {'─'*59}")
