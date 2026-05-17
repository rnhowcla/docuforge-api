@echo off
echo ========================================
echo   DocuForge API - Starting...
echo ========================================

REM Kill existing processes on port 5000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a 2>nul
)

REM Start Flask server
start "DocuForge API" /MIN cmd /c "cd /d D:\克劳德\save && C:\Users\35496\AppData\Local\Programs\Python\Python314\python.exe -X utf8 -m flask --app app.main run --host 127.0.0.1 --port 5000"

REM Wait for Flask to start
timeout /t 3 /nobreak >nul

REM Start SSH tunnel
start "Serveo Tunnel" /MIN bash -c "ssh -o ServerAliveInterval=60 -o StrictHostKeyChecking=no -R 80:localhost:5000 serveo.net 2>&1 | tee /tmp/serveo_url.txt"

echo.
echo Server starting at http://localhost:5000
echo Public URL will appear in the Serveo window.
echo Keep this window open. Close it to stop everything.
echo ========================================
pause
