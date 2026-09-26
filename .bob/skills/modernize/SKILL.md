---
name: modernize
description: Use when the user wants to modernize, migrate, or refactor a legacy JavaScript file — converts callbacks to async/await, var to const/let, runs tests, performs a security audit, and produces a migration report.
---

# BobMigrate Lite — JavaScript Modernization Workflow

Follow every step in order. Do not skip steps. Update the todo list as you progress.

## Step 1 — Identify the Target File

If the user did not specify a file, ask using `ask_followup_question`:
- "Which JavaScript file should I modernize?"

Default to `sample-app/legacy_user_service.js` when running the demo.

## Step 2 — Analyze with detect_legacy_patterns

Call the MCP tool `detect_legacy_patterns` with the target file path.

Parse the returned JSON and display a formatted summary of every finding:
- Line number
- Pattern detected
- Severity (high / medium / low)
- Suggested modernization

If the file is not found, report the error and stop.

## Step 3 — Build a Modernization Plan

Based on the findings, produce a numbered plan before making any changes. Example plan items:
- Replace all `var` declarations with `const` or `let`
- Wrap callback-style functions in a `Promise` constructor
- Convert to `async/await` where possible
- Replace anonymous `function()` with arrow functions
- Remove or replace any deprecated packages detected

Present the plan and proceed (no need to wait for approval in demo mode).

## Step 4 — Apply Changes in Parallel Sub-Agents

Spawn two parallel sub-agents using `spawn_subagent`:

### Refactoring Sub-Agent
Goal: Transform the legacy code.
Instructions:
1. Read the target file with `read_file`.
2. Apply every transformation from the modernization plan:
   - `var` → `const` / `let`
   - Callback-style functions → `Promise` constructor or `async/await`
   - Anonymous `function()` → arrow functions
3. Write the modernized file back with `write_file`, preserving the same file path.
4. Report a summary of all changes made.

### Test Sub-Agent
Goal: Ensure the test file is ready for the modernized code.
Instructions:
1. Read `sample-app/test.js` with `read_file`.
2. Verify the test calls `getUserData(101)` and checks that the result is a Promise
   that resolves with `{ id: 101, name: "Demo User" }`.
3. If the test needs updating (e.g. it still uses callbacks), update it with `write_file`.
4. Report what was verified or changed.

Wait for both sub-agents to complete before continuing.

## Step 5 — Run the Test

Execute:
```
node sample-app/test.js
```
using `execute_command`.

## Step 6 — Self-Heal Loop (max 3 iterations)

If the test **fails**:
1. Read the error output carefully.
2. Identify the root cause (syntax error, wrong API shape, missing export, etc.).
3. Apply a targeted fix to `sample-app/legacy_user_service.js` using `apply_diff` or `search_and_replace`.
4. Re-run `node sample-app/test.js`.
5. Repeat up to 3 times total. If still failing after 3 attempts, report a clear blocking error
   and stop.

If the test **passes**, continue to Step 7.

## Step 7 — Security Audit

Read the final modernized file content with `read_file`, then call the MCP tool `security_audit`
passing the file content as `code_snippet`.

Display the full audit results:
- Total issues found
- For each finding: line, issue title, OWASP category, severity, detail
- Note clearly: "This is a LOCAL rule-based audit — not a watsonx.ai scan."

## Step 8 — Final Migration Report

Produce a structured Markdown migration report with the following sections:

```
# BobMigrate Lite — Migration Report

## Target File
<file path>

## Legacy Patterns Detected
<table: line | pattern | severity | suggestion>

## Modernization Applied
<bulleted list of changes made>

## Files Changed
<list of files modified>

## Tests Executed
- Command: node sample-app/test.js
- Result: PASS / FAIL
- Output: <last test output>

## Security Audit (Local Rule-Based)
<table: line | issue | OWASP category | severity>
OR "No security issues detected."

## Final Status
✅ Modernization complete — all tests pass.
OR
❌ <blocking issue description>
```
