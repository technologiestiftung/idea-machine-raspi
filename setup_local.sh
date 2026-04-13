#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== Local setup: Python venv ==="
python3 -m venv .venv

echo "=== Local setup: pip upgrade ==="
.venv/bin/python -m pip install --upgrade pip

echo "=== Local setup: install requirements ==="
.venv/bin/python -m pip install -r requirements.txt

echo "=== Local setup: .env ==="
if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example"
fi

# Set local default broker IP only if placeholder is still present
if grep -q '^BROKER_IP=xxx\.xxx\.xxx' .env; then
  sed -i.bak 's/^BROKER_IP=.*/BROKER_IP=127.0.0.1/' .env
  rm -f .env.bak
  echo "Set BROKER_IP=127.0.0.1 in .env"
fi

echo "=== Done ==="
echo "Next steps:"
echo "1) Open .env and set MISTRAL_API_KEY + MISTRAL_AGENT_ID"
echo "2) Activate env: source .venv/bin/activate"
echo "3) Run tests: python local_test.py"
