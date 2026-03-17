# 🏥 Clinical MCP Server

A **Model Context Protocol (MCP) server** that exposes two AI-powered tools for processing clinical healthcare documents. Built with Python, FastMCP, and the Anthropic Claude API.

Connect this server to any MCP-compatible client (Claude Desktop, Cursor) and your AI assistant can automatically simplify discharge notes and extract medication data from clinical text.

---

## The Problem

Patients leave hospitals with discharge summaries written by doctors — full of medical jargon, Latin drug names, and clinical abbreviations. Most patients don't understand them, leading to missed medications, skipped follow-ups, and preventable readmissions.

This server addresses that directly.

---

## Tools

### `simplify_clinical_note`
Takes a raw discharge summary and returns a plain-English version a patient can actually understand.

- Replaces medical jargon with everyday language
- Restructures content into clear sections and bullet points
- Covers: what happened, medications, warning signs, follow-up instructions
- Preserves all medical facts — nothing is invented or changed

**Input:** Raw discharge summary text  
**Output:** Patient-friendly plain-English summary

---

### `extract_medications`
Parses a clinical note and returns a structured JSON list of all medications mentioned.

**Input:** Raw clinical note text  
**Output:** JSON array where each object has predefined keys — values pulled directly from the note

```json
[
  {
    "name": "Metformin",
    "dosage": "1000mg",
    "frequency": "twice daily",
    "route": "oral",
    "notes": "take with meals"
  },
  {
    "name": "Insulin Glargine",
    "dosage": "20 units",
    "frequency": "once daily",
    "route": "injection",
    "notes": "at bedtime"
  }
]
```

---

## How It Works

```
You (user)
    │
    ▼
MCP Client (Claude Desktop / Cursor)
    │
    │  MCP Protocol (stdio)
    ▼
Clinical MCP Server  ←── your tools live here
    │
    ▼
Anthropic Claude API  ←── processes the text
    │
    ▼
Result returned to MCP Client → shown to user
```

The MCP layer means these tools are not just scripts — they become callable capabilities that any MCP-compatible AI client can discover and invoke automatically.

---

## Setup

### 1. Clone & install

```bash
git clone https://github.com/Dhruvdd/clinical-mcp-server.git
cd clinical-mcp-server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Add your Anthropic API key to .env
```

### 3. Run the server

```bash
python src/server.py
```

A blinking cursor means it's running and waiting for an MCP client to connect. ✅

---

## Connect to Claude Desktop

Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "clinical-mcp-server": {
      "command": "python",
      "args": ["/absolute/path/to/clinical-mcp-server/src/server.py"]
    }
  }
}
```

Restart Claude Desktop — the two tools will appear automatically.

---

## Connect to Cursor

Add this to Cursor's MCP settings:

```json
{
  "mcpServers": {
    "clinical-mcp-server": {
      "command": "python",
      "args": ["/absolute/path/to/clinical-mcp-server/src/server.py"]
    }
  }
}
```

---

## Tech Stack

- **[FastMCP](https://github.com/jlowin/fastmcp)** — Python MCP server framework
- **[Anthropic Claude API](https://www.anthropic.com)** — LLM for document processing
- **python-dotenv** — environment configuration

---

## Author

**Dhruv Dasadia** — [LinkedIn](https://linkedin.com/in/dhruvdasadia) · [GitHub](https://github.com/Dhruvdd)
