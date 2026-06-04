#!/usr/bin/env bash
set -euo pipefail

# Run this from the project root: ./run_backend.sh
# It starts the Python backend using the package-based backend.app module.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ -d ".venv" ] && [ -f ".venv/bin/activate" ]; then
  # Activate the local virtual environment if present.
  # If you prefer not to use it, unset this or comment it out.
  source ".venv/bin/activate"
fi

export LOCAL_MODEL="${LOCAL_MODEL:-Qwen/Qwen-7B-Chat}"
export ANTHROPIC_API_KEY="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"
export PYTHON_BACKEND_URL="${PYTHON_BACKEND_URL:-http://127.0.0.1:8000/chat}"

echo "Starting backend on http://127.0.0.1:8000"
python3 -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
