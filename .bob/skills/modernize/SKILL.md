---
name: modernize
description: Use when the user wants to modernize, migrate, or refactor a JavaScript file from callbacks to async/await.
---

# BobMigrate Lite - JavaScript Modernization Workflow

Follow every step in order. Do not skip steps.

## Step 1 - Identify Target File
Ask or default to `sample-app/user_service.js`.

## Step 2 - Analyze with detect_legacy_patterns
Call `detect_legacy_patterns` on the file path. Parse JSON results and list findings.

## Step 3 - Refactor Code
Spawn a sub-agent task to rewrite the target file:
- Replace `var` with `const` or `let`.
- Convert callback-based functions to `async function` returning Promises.

## Step 4 - Verify Test Suite Compatibility
Verify `sample-app/test.js` invokes the target function as a Promise.

## Step 5 - Test Execution via Bob Shell
Run `node sample-app/test.js` in Bob Shell terminal.

## Step 6 - Self-Healing Loop
If the test fails (exit code != 0), read the terminal error output, patch `sample-app/user_service.js`, and re-run until `node sample-app/test.js` passes with exit code 0.

## Step 7 - Security Audit
Pass the refactored code into `security_audit` and confirm zero OWASP findings.

## Step 8 - Final Migration Summary
Print a summary showing before vs. after syntax, test results, and security status.
