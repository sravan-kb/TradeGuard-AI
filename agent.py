from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

def analyze_entity(entity_name, screening_result):

    ofac_status = f"MATCH FOUND: {screening_result['matched_ofac']}" if screening_result["ofac_match"] else "No match found"
    sebi_status = f"MATCH FOUND: {screening_result['matched_sebi']}" if screening_result["sebi_match"] else "No match found"

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {
                "role": "user",
                "content": f"""
You are TradeGuard-AI, a compliance screening assistant for vendor due diligence.

Vendor being analyzed: {entity_name}

Screening Results:
- OFAC USA Sanctions: {ofac_status}
- SEBI Debarred India: {sebi_status}

Based on the above screening results, provide a risk assessment.
If a match was found in any dataset, reflect that clearly in your analysis.

Return ONLY in this exact format:

Risk Level: Low, Medium, or High

Vendor Risk:
Assess based on screening results, sector risk, and known issues.

Compliance Risk:
Assess based on sanctions exposure, SEBI debarment, and regulatory standing.

Due Diligence Steps:
List 3 specific actions the compliance team should take.

Key Findings:
Summarize what the screening found and what it means for this vendor.

Keep the response professional and concise.
Do not recommend approving or rejecting. Present findings only.
"""
            }
        ]
    )

    return response.choices[0].message.content