# BobMigrate Lite — MCP Extension & Skill for IBM Bob 2.0

BobMigrate Lite extends **IBM Bob 2.0** with a custom MCP server and agent skill that automates converting legacy JavaScript callbacks to modern `async/await` Promises — with zero LLM token usage for the static analysis, deterministic test validation, and OWASP security scanning.

---

## 🚀 Fresh-Window Setup (do this once after cloning)

### Prerequisites
- **IBM Bob 2.0** installed
- **Python 3.8+** (`python3 --version`)
- **Node.js 16+** (`node --version`)

### 1. Clone and install

```bash
git clone <repo-url>
cd bob-migrate
bash setup.sh
```

`setup.sh` will:
- Verify Python and Node.js are present
- Install `mcp<2` and `requests` via pip
- Smoke-test the MCP server
- Run the JS test fixtures

### 2. Open in IBM Bob 2.0

Open the cloned folder as your workspace in IBM Bob 2.0.
Bob will automatically pick up `.bob/mcp.json` (registering the MCP server) and `.bob/skills/modernize/SKILL.md` (activating the skill).

### 3. Run the modernization

In IBM Bob Agent Mode, type:
```
Modernize sample-app/user_service.js
```

Bob will run the full 9-step pipeline automatically.

---

## 🌟 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    IBM Bob 2.0 Agent                    │
│                                                         │
│  .bob/skills/modernize/SKILL.md  ←  9-step workflow     │
│         │                                               │
│         │  calls MCP tools                              │
│         ▼                                               │
│  .bob/mcp.json  →  mcp-server/server.py (Python)        │
│                        │                                │
│                        ├─ detect_legacy_patterns()      │
│                        └─ security_audit()              │
│                                                         │
│  Bob Shell: node sample-app/test.js  (exit 0 = pass)   │
└─────────────────────────────────────────────────────────┘
```

1. **`mcp-server/server.py`** — FastMCP server running over `stdio`. Provides two off-LLM, zero-token static analysis tools.
2. **`.bob/skills/modernize/SKILL.md`** — Teaches Bob's Agent how to execute the full pipeline: analyze → refactor → test → self-heal → audit → report.
3. **`sample-app/test.js`** — Deterministic test runner. Passes only if `getUserData` returns a real `Promise` — no LLM assumptions.

---

## 📁 Repository Structure

```
bob-migrate/
├── .bob/
│   ├── mcp.json                      # Registers the MCP server with Bob
│   └── skills/
│       └── modernize/
│           └── SKILL.md              # 9-step agent workflow
├── mcp-server/
│   ├── server.py                     # Python MCP server (2 tools)
│   └── requirements.txt              # mcp<2, requests
├── sample-app/
│   ├── user_service.js               # ← TARGET: legacy JS (var + callbacks + http.get)
│   ├── legacy_user_service.js        # Reference: what user_service.js looks like after modernization
│   └── test.js                       # Bob Shell test runner (Promise assertion)
├── test-fixtures/
│   ├── legacy.js                     # Fixture: Promise-based getUserData
│   ├── legacy.test.js                # Test for legacy.js fixture
│   └── legacy_with_callbacks.js      # Demo: true legacy JS for detect_legacy_patterns showcase
├── docs/
│   └── screenshots/
│       └── task_summary.png
├── setup.sh                          # One-shot environment installer
├── .gitignore
├── .bobignore
└── README.md
```

---

## 🔧 MCP Tools

Both tools run entirely in Python — no LLM tokens consumed, deterministic output.

### `detect_legacy_patterns(file_path)`

Scans any `.js` file for deprecated syntax patterns by reading file content.

Detects:
| Pattern | Severity | Suggestion |
|---|---|---|
| `var` declaration | low | Use `const` or `let` |
| Callback pattern (`function(err, cb)`) | high | Refactor to `async/await` |
| `http.get()` call | medium | Use `fetch` or Promise wrapper |

Returns structured JSON with line numbers, severity ratings, and suggestions.

**Example:**
```json
{
  "file": "sample-app/user_service.js",
  "total_issues": 7,
  "findings": [
    { "line": 5, "pattern": "var declaration", "severity": "low", "suggestion": "Use const or let" },
    { "line": 8, "pattern": "callback pattern", "severity": "high", "suggestion": "Refactor to async/await Promise" }
  ]
}
```

### `security_audit(code_snippet)`

Performs a deterministic OWASP-baseline security scan on any code string.

Detects:
| Vulnerability | Severity |
|---|---|
| `eval()` usage | CRITICAL |
| Hardcoded credentials (`api_key`, `password`, `secret`) | HIGH |

Returns `PASSED` or `FAILED` with a count of findings.

---

## 🛡️ Guarantees

| Guarantee | How |
|---|---|
| **No hallucination** | `node sample-app/test.js` must exit 0 — actual code execution, not LLM opinion |
| **Content-based analysis** | `detect_legacy_patterns` reads file bytes, not filename |
| **Zero token cost for analysis** | Both MCP tools run in Python off-LLM |
| **Self-healing** | If the test fails, the skill patches the file and retries up to 3× |
| **Context-safe** | Only JSON findings metadata enters the LLM context, not raw file dumps |

---

## 🧪 Running Tests Manually

```bash
# Test the sample app (should FAIL before modernization — legacy file)
node sample-app/test.js

# Test the fixtures
node test-fixtures/legacy.test.js

# Smoke-test MCP tools directly
python3 -c "
import sys; exec(open('mcp-server/server.py').read().replace('mcp.run()', ''))
print(detect_legacy_patterns('test-fixtures/legacy_with_callbacks.js'))
"
```
