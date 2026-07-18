#!/usr/bin/env bash
set -o errexit
set -o pipefail

echo "[1/7] Starting build..."
python --version
pip --version

echo "[2/7] Cleaning cached artifacts..."
rm -rf venv
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

echo "[3/7] Creating fresh venv..."
python -m venv venv
. venv/bin/activate

echo "[4/7] Upgrading pip and installing deps..."
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

echo "[5/7] Verify user_agents..."
python -c "from user_agents import parse; print('OK:', parse('test'))"

echo "[6/7] Collectstatic..."
python manage.py collectstatic --no-input

echo "[7/7] Migrate..."
python manage.py migrate --no-input

echo "BUILD SUCCESS"
