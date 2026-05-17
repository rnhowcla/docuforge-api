#!/bin/bash
echo "====================================="
echo " DocuForge API - Starting..."
echo "====================================="

cd "D:\克劳德\save"

# Start Flask
/c/Users/35496/AppData/Local/Programs/Python/Python314/python.exe -X utf8 -m flask --app app.main run --host 127.0.0.1 --port 5000 &
FLASK_PID=$!
sleep 3

echo "Flask started on http://127.0.0.1:5000"
echo ""

# Try pinggy.io instead of serveo (serveo unreliable in CN)
echo "Trying pinggy.io tunnel..."
echo "Your public URL will appear below:"
echo "====================================="
ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -R 0:localhost:5000 -p 443 a.pinggy.io

# If pinggy fails, kill Flask
kill $FLASK_PID 2>/dev/null
