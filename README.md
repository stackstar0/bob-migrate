# BobMigrate Lite — MCP Extension & Skill Package for IBM Bob 2.0

BobMigrate Lite extends **IBM Bob 2.0** with custom static analysis tools and a self-healing modernization skill that automates converting legacy JavaScript callbacks to modern `async/await` Promises.

## 🌟 Architecture Overview

1. **Custom FastMCP Server (`mcp-server/server.py`):** Runs locally via `stdio` protocol to provide off-LLM, zero-token pattern detection (`detect_legacy_patterns`) and security auditing (`security_audit`).
2. **Custom Agent Skill (`.bob/skills/modernize/SKILL.md`):** Teaches Bob's Agent Mode how to execute an 8-step pipeline covering analysis, refactoring, Bob Shell testing, self-healing, and auditing.
3. **Deterministic Test Loop:** Uses Bob Shell terminal execution (`node sample-app/test.js`) to guarantee code correctness without relying on LLM assumptions.

## 🚀 Quickstart Guide

1. Clone this repository.
2. Open the repository in **IBM Bob 2.0**.
3. Install Python dependencies:
   ```bash
   pip install mcp
   ```
4. In IBM Bob Chat, select Agent Mode and run:
   ```
   Modernize sample-app/user_service.js
   ```

## 📁 Repository Structure

```
bobmigrate-mcp/
├── .bob/
│   ├── mcp.json                        # Tells Bob to launch server.py
│   └── skills/
│       └── modernize/
│           └── SKILL.md                # Standardized 8-step agent workflow
├── mcp-server/
│   ├── server.py                       # Python FastMCP server (2 tools)
│   └── requirements.txt                # Dependencies (mcp, requests)
├── sample-app/
│   ├── user_service.js                 # Target legacy JS file
│   └── test.js                         # Deterministic Promise test runner
├── docs/
│   └── screenshots/
│       └── task_summary.png            # Bob 2.0 execution screenshot
├── .gitignore
├── .bobignore
└── README.md
```

## 🔧 MCP Tools

### `detect_legacy_patterns(file_path)`
Scans any JavaScript file for deprecated syntax **by reading file content** — not by filename. Detects:
- `var` declarations → suggest `const`/`let`
- Callback patterns → suggest `async/await`
- `http.get()` usage → suggest `fetch`/`axios`

Returns structured JSON with line numbers, severity ratings, and suggestions.

### `security_audit(code_snippet)`
Performs a deterministic, off-LLM OWASP security scan for:
- `eval()` usage (CRITICAL)
- Hardcoded credentials/secrets (HIGH)

Returns PASSED/FAILED status with findings count.

## 🛡️ What This Implementation Guarantees

1. **Content-Based Analysis:** Rename `user_service.js` to anything — `detect_legacy_patterns` still reads file content and finds legacy patterns.
2. **True MCP Value:** Python handles heavy string parsing on disk at 0 LLM tokens, returning structured JSON metadata to Bob.
3. **No Hallucination:** The system runs `node sample-app/test.js` in Bob Shell. The test passes only if the code actually executes correctly.
4. **Context Window Safety:** Large codebases aren't dumped into context windows — only JSON findings from target files are processed by sub-agents.
