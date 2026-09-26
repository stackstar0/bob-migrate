#!/usr/bin/env python3
"""
BobMigrate Lite — MCP Server
Provides tools for detecting legacy JavaScript patterns and performing
a local (deterministic) security audit.
"""

import json
import re
import sys
from pathlib import Path

from fastmcp import FastMCP

mcp = FastMCP("bobmigrate-lite")

# ---------------------------------------------------------------------------
# Pattern definitions
# ---------------------------------------------------------------------------

LEGACY_PATTERNS = [
    {
        "id": "var_declaration",
        "regex": re.compile(r"\bvar\s+\w+"),
        "pattern": "var declaration",
        "severity": "low",
        "suggestion": "Replace 'var' with 'const' (immutable) or 'let' (mutable).",
    },
    {
        "id": "callback_last_arg",
        "regex": re.compile(r"\bfunction\s*\([^)]*\bcallback\b[^)]*\)"),
        "pattern": "callback-style function signature",
        "severity": "high",
        "suggestion": "Convert to an async function that returns a Promise.",
    },
    {
        "id": "callback_invocation",
        "regex": re.compile(r"\bcallback\s*\("),
        "pattern": "callback invocation",
        "severity": "high",
        "suggestion": "Replace callback(err, result) calls with resolve(result) / reject(err) inside a Promise constructor, or use async/await.",
    },
    {
        "id": "anonymous_function_expression",
        "regex": re.compile(r"\bfunction\s*\("),
        "pattern": "anonymous function expression",
        "severity": "medium",
        "suggestion": "Replace with an arrow function: (...) => { ... }",
    },
    {
        "id": "legacy_require_http",
        "regex": re.compile(r"\brequire\s*\(\s*['\"]http['\"]\s*\)"),
        "pattern": "legacy http.request pattern",
        "severity": "medium",
        "suggestion": "Use the built-in fetch() API (Node 18+) or a modern library like axios/got.",
    },
    {
        "id": "legacy_require_request",
        "regex": re.compile(r"\brequire\s*\(\s*['\"]request['\"]\s*\)"),
        "pattern": "deprecated 'request' package",
        "severity": "high",
        "suggestion": "The 'request' package is deprecated. Migrate to fetch() or axios.",
    },
]

SECURITY_PATTERNS = [
    {
        "id": "eval_usage",
        "regex": re.compile(r"\beval\s*\("),
        "title": "eval() usage",
        "owasp": "A03:2021 – Injection",
        "severity": "critical",
        "detail": "eval() executes arbitrary code. Remove it and use safer alternatives.",
    },
    {
        "id": "innerhtml_assignment",
        "regex": re.compile(r"\.innerHTML\s*="),
        "title": "innerHTML assignment",
        "owasp": "A03:2021 – Injection (XSS)",
        "severity": "high",
        "detail": "Direct innerHTML assignment can introduce XSS. Use textContent or a sanitiser.",
    },
    {
        "id": "document_write",
        "regex": re.compile(r"\bdocument\.write\s*\("),
        "title": "document.write() usage",
        "owasp": "A03:2021 – Injection (XSS)",
        "severity": "high",
        "detail": "document.write() can be exploited for XSS. Prefer DOM manipulation APIs.",
    },
    {
        "id": "hardcoded_secret",
        "regex": re.compile(
            r'(?:password|secret|api_?key|token)\s*[=:]\s*["\'][^"\']{6,}["\']',
            re.IGNORECASE,
        ),
        "title": "Hardcoded credential",
        "owasp": "A02:2021 – Cryptographic Failures",
        "severity": "critical",
        "detail": "Store secrets in environment variables or a secrets manager, not in source code.",
    },
    {
        "id": "sql_string_concat",
        "regex": re.compile(r'(?:SELECT|INSERT|UPDATE|DELETE).*\+\s*\w', re.IGNORECASE),
        "title": "Possible SQL string concatenation",
        "owasp": "A03:2021 – Injection (SQLi)",
        "severity": "high",
        "detail": "String-concatenated SQL queries are vulnerable to injection. Use parameterised queries.",
    },
    {
        "id": "console_log_sensitive",
        "regex": re.compile(
            r'console\.log\s*\(.*(?:password|token|secret|key)',
            re.IGNORECASE,
        ),
        "title": "Potential sensitive data logged",
        "owasp": "A09:2021 – Security Logging and Monitoring Failures",
        "severity": "medium",
        "detail": "Logging sensitive values exposes them in log aggregators. Redact before logging.",
    },
]


# ---------------------------------------------------------------------------
# Tool 1 — detect_legacy_patterns
# ---------------------------------------------------------------------------

@mcp.tool
def detect_legacy_patterns(file_path: str) -> str:
    """
    Scan a JavaScript file for legacy coding patterns (var, callbacks, etc.)
    and return a structured JSON report with line numbers, pattern descriptions,
    severity ratings, and modernisation suggestions.
    """
    path = Path(file_path)
    if not path.exists():
        return json.dumps({"error": f"File not found: {file_path}"}, indent=2)

    findings: list[dict] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return json.dumps({"error": str(exc)}, indent=2)

    for lineno, line in enumerate(lines, start=1):
        for pat in LEGACY_PATTERNS:
            if pat["regex"].search(line):
                findings.append(
                    {
                        "file": str(path),
                        "line": lineno,
                        "code_snippet": line.strip(),
                        "pattern": pat["pattern"],
                        "severity": pat["severity"],
                        "suggested_modernization": pat["suggestion"],
                    }
                )

    result = {
        "file": str(path),
        "total_findings": len(findings),
        "findings": findings,
    }
    return json.dumps(result, indent=2)


# ---------------------------------------------------------------------------
# Tool 2 — security_audit
# ---------------------------------------------------------------------------

@mcp.tool
def security_audit(code_snippet: str) -> str:
    """
    Perform a deterministic LOCAL security scan of the supplied JavaScript code
    for selected OWASP-related patterns.

    NOTE: This is a local, rule-based audit — NOT a watsonx.ai or AI-powered
    analysis. Results are based solely on regex pattern matching.
    """
    findings: list[dict] = []
    lines = code_snippet.splitlines()

    for lineno, line in enumerate(lines, start=1):
        for pat in SECURITY_PATTERNS:
            if pat["regex"].search(line):
                findings.append(
                    {
                        "line": lineno,
                        "code_snippet": line.strip(),
                        "issue": pat["title"],
                        "owasp_category": pat["owasp"],
                        "severity": pat["severity"],
                        "detail": pat["detail"],
                    }
                )

    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    findings.sort(key=lambda f: severity_order.get(f["severity"], 9))

    result = {
        "audit_type": "LOCAL rule-based security scan (not watsonx.ai)",
        "total_findings": len(findings),
        "findings": findings,
        "summary": "No security issues detected." if not findings else (
            f"{len(findings)} issue(s) found. Review findings above."
        ),
    }
    return json.dumps(result, indent=2)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run(transport="stdio")
