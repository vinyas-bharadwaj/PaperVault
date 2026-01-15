#!/bin/bash

lsof -ti:8000 | xargs kill -9 2>/dev/null; echo "Killed processes on port 8000"
lsof -ti:5173 | xargs kill -9 2>/dev/null; echo "Killed processes on port 5173"

docker compose up -d

cd server && python -m uvicorn app.main:app --reload &
cd client && npm run dev &

wait
