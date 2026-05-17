#!/bin/bash
echo "====================================="
echo " DocuForge API - Starting..."
echo "====================================="

# Start Flask
cd "D:\克劳德\save"
/c/Users/35496/AppData/Local/Programs/Python/Python314/python.exe -X utf8 -m flask --app app.main run --host 127.0.0.1 --port 5000 &
FLASK_PID=$!
sleep 2

# Start tunnel
echo ""
echo "Opening tunnel to serveo.net..."
echo "Your public URL will appear below:"
echo "====================================="
ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -R 80:localhost:5000 serveo.net

# When SSH exits, kill Flask
kill $FLASK_PID 2>/dev/null
