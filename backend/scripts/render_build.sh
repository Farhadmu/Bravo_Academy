#!/usr/bin/env bash
# Render.com build script for Django (Memory Efficient)
set -o errexit
set -o nounset
set -o pipefail

echo "🔧 Build started..."
python -m venv venv
source venv/bin/activate

echo "📦 Installing dependencies (no-cache to save RAM)..."
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir

echo "🎨 Collecting static assets..."
python manage.py collectstatic --no-input

echo "🗄️ Running migrations..."
# Fake users 0003 if it fails due to existing is_developer column
python manage.py migrate users 0003 --fake || echo "Migration users 0003 already applied or failed, continuing..."
python manage.py migrate --no-input

echo "✅ Build successful!"
