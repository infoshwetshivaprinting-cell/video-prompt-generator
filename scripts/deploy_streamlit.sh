#!/usr/bin/env bash
# Deployment helper script for local testing and deploying to Streamlit Community Cloud.
# Note: Streamlit Community Cloud deploys from your GitHub repository using the UI.

set -e

usage() {
  echo "Usage: $0 [run|check]"
  echo "  run   - Run the Streamlit app locally"
  echo "  check - Validate environment and requirements"
  exit 1
}

if [ "$1" == "run" ]; then
  echo "Starting Streamlit app locally..."
  if [ ! -f requirements.txt ]; then
    echo "requirements.txt not found. Create one before running locally."
    exit 1
  fi
  python -m streamlit run streamlit_app.py
  exit 0
fi

if [ "$1" == "check" ]; then
  echo "Checking for common requirements..."
  python - << 'PY'
import sys
import importlib
reqs = ['streamlit','moviepy','PIL']
missing = []
for r in reqs:
    try:
        importlib.import_module(r)
    except Exception:
        missing.append(r)
if missing:
    print('Missing packages:', missing)
    sys.exit(2)
print('All quick checks passed.')
PY
  exit 0
fi

usage
