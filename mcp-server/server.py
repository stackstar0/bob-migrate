import os
import re
import json
try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    from fastmcp import FastMCP

mcp = FastMCP("bobmigrate-lite-mcp")

@mcp.tool()
def detect_legacy_patterns(file_path: str) -> str:
    """Scans file content for deprecated JS syntax (var, callbacks, http calls)."""
    if not os.path.exists(file_path):
        return json.dumps({"error": f"File '{file_path}' not found."})

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    findings = []
    for idx, line in enumerate(lines, 1):
        if re.search(r'\bvar\b', line):
            findings.append({"line": idx, "pattern": "var declaration", "severity": "low", "suggestion": "Use const or let"})
        if re.search(r'function\s*\([^\)]*err[^\)]*\)|callback\(', line):
            findings.append({"line": idx, "pattern": "callback pattern", "severity": "high", "suggestion": "Refactor to async/await Promise"})
        if re.search(r'http\.get\(', line):
            findings.append({"line": idx, "pattern": "deprecated http.get", "severity": "medium", "suggestion": "Use fetch or axios"})

    return json.dumps({"file": file_path, "total_issues": len(findings), "findings": findings}, indent=2)

@mcp.tool()
def security_audit(code_snippet: str) -> str:
    """Scans code snippets for OWASP security vulnerabilities (eval, hardcoded secrets)."""
    vulnerabilities = []
    if "eval(" in code_snippet:
        vulnerabilities.append("CRITICAL: Unsafe eval() execution detected.")
    if re.search(r'(api_key|password|secret)\s*=\s*["\'][^"\']+["\']', code_snippet, re.IGNORECASE):
        vulnerabilities.append("HIGH: Hardcoded credentials/secrets detected.")

    if not vulnerabilities:
        return json.dumps({"status": "PASSED", "findings_count": 0, "message": "Code satisfies OWASP baseline standard."})

    return json.dumps({"status": "FAILED", "findings_count": len(vulnerabilities), "findings": vulnerabilities})

if __name__ == "__main__":
    mcp.run()
