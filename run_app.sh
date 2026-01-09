#!/bin/bash

echo "Starting Backend..."
uvicorn backend.app.main:app --port 8000 &
BACKEND_PID=$!

echo "Waiting for Backend to initialize..."
sleep 3

echo "Starting Frontend..."
streamlit run frontend/app.py &
FRONTEND_PID=$!

# Trap Ctrl+C to kill both processes
trap "kill $BACKEND_PID $FRONTEND_PID; exit" SIGINT

echo "App is running! Press Ctrl+C to stop."
wait
