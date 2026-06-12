from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

def analyze_entity(entity_name, screening_result):

    ofac_status = f"MATCHES FOUND: {', '.join(screening_result['matched_ofac'])}" if screening_result["ofac_match"] else "No match found"
    sebi_status = f"MATCHES FOUND: {', '.join(screening_result['matched_sebi'])}" if screening_result["sebi_match"] else "No match found"

    any_match = screening_result["ofac_match"] or screening_result["sebi_match"]
    match_summary = "ONE OR MORE MATCHES FOUND — ELEVATED RISK" if any_match else "NO MATCHES FOUND — PROCEED WITH STANDARD DUE DILIGENCE"

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {
                "role": "system",
                "content": (
                    "You are TradeGuard-AI, a senior compliance analyst writing structured vendor risk reports. "
                    "Your reports are read by compliance officers who need clear, direct, actionable findings. "
                    "You never approve or reject vendors. You present facts, assess risk, and recommend specific actions. "
                    "Avoid filler phrases, vague language, and repetition. Every sentence must add value. "
                    "CRITICAL: Never repeat any section. Each section appears exactly once. "
                    "Number lists sequentially: 1. then 2. then 3. Never use 1. more than once."
                )
            },
            {
                "role": "user",
                "content": f"""
You are a senior compliance analyst. Generate a structured vendor screening report.

VENDOR: {entity_name}
OFAC STATUS: {ofac_status}
SEBI STATUS: {sebi_status}

RULES:
1. Only reference datasets that have matches
2. For each matched entity, explain in one sentence what it is and why it may be sanctioned/debarred — use your knowledge. If unknown, say "reason for listing not available"
3. State clearly if matched entities are the same or different legal entity from {entity_name}
4. Risk: Low = no match, Medium = different entity with similar name, High = same or near-identical entity
5. No filler phrases. Every sentence must be factual and direct
6. Due diligence steps must be specific to {entity_name} — not copy-paste advice
7. If all matched entities are clearly different from {entity_name}, COMPLIANCE EXPOSURE should state: "No direct compliance exposure identified. The matched entities are distinct legal entities. Standard vendor onboarding compliance applies." Do not invent hypothetical risks for clean vendors.
8. Number due diligence actions sequentially as 1. then 2. then 3. — never repeat the same number
9. First check: if VENDOR name appears to be a person's name (e.g. "Raj Kumar", "John Smith", "Amit Shah") and not a company, respond with only this single word: PERSON_DETECTED

RESPOND EXACTLY IN THIS FORMAT — EACH SECTION APPEARS ONCE AND ONLY ONCE:

RISK LEVEL: High / Medium / Low

COMPANY OVERVIEW:
2-3 sentences. What is {entity_name}? What sector, country, what do they do? If well known, state that. If unknown, say "Limited public information available on this entity."

SCREENING SUMMARY:
[What was found. For each match: name it, what it is, why sanctioned/debarred in one sentence. State if same or different from {entity_name}.]

VENDOR RISK ANALYSIS:
[What this means for onboarding {entity_name}. Be direct.]

COMPLIANCE EXPOSURE:
[Specific regulatory consequences if vendor is confirmed as matched entity.]

RECOMMENDED DUE DILIGENCE ACTIONS:
1. [Action specific to findings]
2. [Action specific to {entity_name} sector]
3. [Ongoing monitoring action]

IMPORTANT NOTICE:
This report is for informational purposes only. Final vendor decisions rest with the compliance officer.
"""
            }
        ]
    )

    return response.choices[0].message.content