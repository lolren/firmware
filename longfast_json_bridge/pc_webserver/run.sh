#!/usr/bin/env bash
set -euo pipefail

NODE_URL="${1:-http://192.168.1.100}"
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8765}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 "${SCRIPT_DIR}/longfast_json_bridge_web.py" \
  --host "${HOST}" \
  --port "${PORT}" \
  --esp-base-url "${NODE_URL}"
