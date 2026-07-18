#!/usr/bin/env bash
# Render.com build script for Django (Memory Efficient, Fixed LF line endings)
set -o errexit
set -o pipefail
# Note: nounset intentionally omitted because Render build env may have unset variables

echo "Build started..."
python -m venv venv
source venv/bin/activate

echo "Installing dependencies (no-cache to save RAM)..."
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir

echo "Verifying critical imports..."
python -c "from user_agents import parse; print('user-agents OK')" 2>&1 || echo "WARNING: user-agents check failed"

echo "Collecting static assets..."
python manage.py collectstatic --no-input

echo "Running migrations..."
python manage.py migrate --no-input

echo "Build successful!"
