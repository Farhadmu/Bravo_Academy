#!/usr/bin/env bash
set -o errexit
set -o pipefail

echo "[1/6] Starting build..."
python --version
pip --version

echo "[2/6] Cleaning and creating fresh venv..."
rm -rf venv
python -m venv venv
. venv/bin/activate

echo "[3/6] Upgrading pip and installing deps..."
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

echo "[4/6] Verify user_agents..."
python -c "from user_agents import parse; print('OK:', parse('test'))"

echo "[5/6] Collectstatic..."
python manage.py collectstatic --no-input

echo "[6/6] Migrate..."
python manage.py migrate --no-input

echo "BUILD SUCCESS"
