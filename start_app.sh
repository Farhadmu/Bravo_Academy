#!/bin/bash
cd backend
source venv/bin/activate
echo "Running migrations..."
python manage.py migrate
echo "Starting backend..."
python manage.py runserver 0.0.0.0:8000 > backend.log 2>&1 &
cd ../frontend
echo "Starting frontend..."
npm run dev -- --port 3000 > frontend.log 2>&1 &
sleep 10
