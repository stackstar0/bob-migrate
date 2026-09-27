#!/usr/bin/env bash
# setup.sh — BobMigrate Lite one-shot environment setup
# Run this once after cloning: bash setup.sh

set -e

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║        BobMigrate Lite — Environment Setup           ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# ── 1. Check required runtimes ──────────────────────────────
echo "[ 1/4 ] Checking runtime dependencies..."

if ! command -v python3 &>/dev/null; then
  echo "  ✗ python3 not found. Install Python 3.8+ and re-run."
  exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1)
echo "  ✓ $PYTHON_VERSION"

if ! command -v node &>/dev/null; then
  echo "  ✗ node not found. Install Node.js 16+ and re-run."
  exit 1
fi
NODE_VERSION=$(node --version 2>&1)
echo "  ✓ Node.js $NODE_VERSION"

# ── 2. Install Python dependencies ──────────────────────────
echo ""
echo "[ 2/4 ] Installing Python dependencies (mcp<2, requests)..."
pip install -r mcp-server/requirements.txt --quiet
echo "  ✓ Python packages installed."

# ── 3. Verify MCP server loads ───────────────────────────────
echo ""
echo "[ 3/4 ] Verifying MCP server..."
python3 -c "
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath('.')), 'mcp-server'))
exec(open('mcp-server/server.py').read().replace('mcp.run()', 'print(\"  ✓ MCP server: bobmigrate-lite-mcp — OK\")'))
"

# ── 4. Run JS test suites ────────────────────────────────────
echo ""
echo "[ 4/4 ] Running JavaScript test suites..."

echo "  → test-fixtures/legacy.test.js"
node test-fixtures/legacy.test.js 2>&1 | sed 's/^/      /'

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  ✅  Setup complete. Open this repo in IBM Bob 2.0"
echo "      and run:  Modernize sample-app/user_service.js"
echo "═══════════════════════════════════════════════════════"
echo ""
