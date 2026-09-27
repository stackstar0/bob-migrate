---
name: modernize
description: Use when the user wants to modernize, migrate, or refactor a JavaScript file from callbacks to async/await.
---

# BobMigrate Lite — JavaScript Modernization Workflow

Follow every step in order. Do not skip or reorder steps.

---

## Step 1 — Identify Target File

Ask the user which JavaScript file to modernize.
If no file is specified, default to `sample-app/user_service.js`.
Store the path as `TARGET_FILE`.

---

## Step 2 — Analyze with `detect_legacy_patterns`

Call the MCP tool `detect_legacy_patterns` with `file_path = TARGET_FILE`.

Parse the JSON response and print a formatted findings table:
- Total issues found
- Each finding: line number, pattern type, severity, suggestion

If `total_issues === 0`, inform the user the file is already modern and stop here.

---

## Step 3 — Snapshot the Original

Read `TARGET_FILE` and store its contents as `ORIGINAL_CODE` for the before/after summary in Step 8.

---

## Step 4 — Refactor the Code

Rewrite `TARGET_FILE` applying ALL of the following transformations:
- Replace every `var` declaration with `const` or `let` (use `const` when the binding is never reassigned).
- Convert every callback-based function (`function(err, result)` pattern) to an `async function` that returns a `Promise`.
- Replace `http.get()` calls with `fetch()` or a `new Promise()` wrapper using the built-in `http` module if `fetch` is unavailable in Node.
- Preserve all existing exports (`module.exports`).
- Do not change the function's external API (same function name, same arguments minus the callback).

Write the refactored code back to `TARGET_FILE`.

---

## Step 5 — Verify Test Suite Compatibility

Read `sample-app/test.js`.
Confirm it calls `getUserData` without a callback and checks `result.then` — i.e., it expects a Promise.
If the test file tests a different function than what you refactored, note the mismatch but continue.

---

## Step 6 — Test Execution via Bob Shell

Run in the terminal:
```
node sample-app/test.js
```

If the exit code is 0 and output contains `✅ TEST PASSED`, continue to Step 7.

---

## Step 7 — Self-Healing Loop

If the test exits with code != 0:
1. Read the full terminal error output.
2. Identify the specific line or pattern causing the failure.
3. Patch `TARGET_FILE` to fix the issue.
4. Re-run `node sample-app/test.js`.
5. Repeat up to **3 times**. If still failing after 3 attempts, report the error and stop.

---

## Step 8 — Security Audit

Read the full contents of `TARGET_FILE`.
Pass the code as a string to the MCP tool `security_audit`.

- If status is `PASSED` → confirm zero OWASP findings.
- If status is `FAILED` → list each finding and fix the issue in the file before completing.

---

## Step 9 — Final Migration Summary

Print a structured summary:

```
╔══════════════════════════════════════════════╗
║       BobMigrate Lite — Migration Report     ║
╚══════════════════════════════════════════════╝

File:         <TARGET_FILE>
Issues found: <N from Step 2>

BEFORE (legacy patterns detected):
  • <list each finding from Step 2>

AFTER (transformations applied):
  • var → const/let
  • callbacks → async/await Promise
  • http.get → Promise wrapper

Test result:  ✅ PASSED  (node sample-app/test.js exit 0)
Security:     ✅ PASSED  (0 OWASP findings)
```
