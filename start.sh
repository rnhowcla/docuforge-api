#!/bin/bash
echo "====================================="
echo " DocuForge API - Starting..."
echo "====================================="

# Generate SSH key if missing
if [ ! -f ~/.ssh/id_ed25519 ]; then
    echo "Generating SSH key..."
    ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N "" -q
fi

cd "D:\克劳德\save"

# Start Flask
/c/Users/35496/AppData/Local/Programs/Python/Python314/python.exe -X utf8 -m flask --app app.main run --host 127.0.0.1 --port 5000 &
FLASK_PID=$!
sleep 3

echo "Flask started on http://127.0.0.1:5000"
echo ""

# Start tunnel via localhost.run
echo "Opening tunnel via localhost.run..."
echo "Your public URL is the https://*.lhr.life address below:"
echo "====================================="
ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -R 80:127.0.0.1:5000 localhost.run

kill $FLASK_PID 2>/dev/null
