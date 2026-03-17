"""
Clinical MCP Server
A Model Context Protocol (MCP) server exposing tools for clinical note processing.

Tools:
  - simplify_clinical_note : converts a discharge summary into plain-English
  - extract_medications     : returns a structured list of medications from a note
"""

import json
import os
import anthropic
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    base_url=os.getenv("ANTHROPIC_BASE_URL")
)
mcp = FastMCP("clinical-mcp-server")


# ── Tool 1: Simplify Clinical Note ────────────────────────────────────────────

@mcp.tool()
def simplify_clinical_note(clinical_note: str) -> str:
    """
    Takes a raw clinical discharge summary and returns a simplified,
    patient-friendly plain-English version that a non-medical person can understand.

    Args:
        clinical_note: The raw discharge summary or clinical note text.

    Returns:
        A plain-English summary with clear instructions the patient can follow.
    """
    system_prompt = """You are a medical communication assistant. Your job is to take 
clinical discharge summaries written by doctors and rewrite them in simple, 
friendly language that a patient with no medical background can easily understand.

Rules:
- Replace all medical jargon with plain English equivalents
- Use short sentences and bullet points for instructions
- Keep a warm, reassuring tone
- Always include: diagnosis explanation, medications with simple instructions, 
  warning signs to watch for, and follow-up instructions
- Never invent or change any medical facts from the original note"""

    response = client.messages.create(
        model="global.anthropic.claude-opus-4-6",
        max_tokens=800,
        system=system_prompt,
        messages=[
            {"role": "user", "content": f"Please simplify this discharge summary:\n\n{clinical_note}"}
        ]
    )

    return response.content[0].text


# ── Tool 2: Extract Medications ────────────────────────────────────────────────

@mcp.tool()
def extract_medications(clinical_note: str) -> str:
    """
    Parses a clinical note and extracts a structured list of all medications
    including dosage, frequency, and route of administration.

    Args:
        clinical_note: The raw clinical note or discharge summary text.

    Returns:
        A JSON string containing a list of medication objects with fields:
        name, dosage, frequency, route, and notes.
    """
    system_prompt = """You are a clinical data extraction assistant. Extract all medications 
from the provided clinical note and return them as a JSON array.

Each medication object must have these fields:
- "name": medication name (string)
- "dosage": dose amount and unit e.g. "500mg" (string)
- "frequency": how often e.g. "twice daily" (string)  
- "route": how taken e.g. "oral", "injection", "inhaler" (string)
- "notes": any special instructions e.g. "take with meals", "at bedtime" (string, can be empty)

Return ONLY valid JSON. No explanation text, no markdown fences."""

    response = client.messages.create(
        model="global.anthropic.claude-opus-4-6",
        max_tokens=600,
        system=system_prompt,
        messages=[
            {"role": "user", "content": f"Extract all medications from this note:\n\n{clinical_note}"}
        ]
    )

    raw = response.content[0].text.strip()

    # Validate it's real JSON before returning
    try:
        parsed = json.loads(raw)
        return json.dumps(parsed, indent=2)
    except json.JSONDecodeError:
        return json.dumps({"error": "Could not parse medications from note", "raw": raw})


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run(transport="stdio")