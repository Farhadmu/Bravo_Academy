#!/usr/bin/env bash
set -o errexit
set -o pipefail

echo "[1/6] Starting build..."
python --version
pip --version

echo "[2/6] Cleaning cached artifacts and creating fresh venv..."
rm -rf venv
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
python -m venv venv
. venv/bin/activate

echo "[3/6] Installing dependencies..."
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

echo "[4/6] Collecting static assets..."
python manage.py collectstatic --no-input

echo "[5/6] Running database migrations..."
python manage.py migrate --no-input

echo "[6/6] Build completed successfully!"
