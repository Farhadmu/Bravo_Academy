#!/usr/bin/env bash
set -o errexit
set -o pipefail

echo "[1/5] Starting build..."
python --version
pip --version

echo "[2/5] Creating fresh venv..."
rm -rf venv
python -m venv venv
. venv/bin/activate

echo "[3/5] Installing dependencies..."
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

echo "[4/5] Building Django assets..."
python manage.py collectstatic --no-input
python manage.py migrate --no-input

echo "[5/5] Build completed successfully!"
