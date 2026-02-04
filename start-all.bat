@echo off
echo ========================================
echo Starting Voice Agent Application (DAY2)
echo ========================================
echo.

echo [1/3] Starting LiveKit Server...
start "LiveKit Server" cmd /k "C:\LiveKit\livekit-server.exe --dev"
timeout /t 3 /nobreak >nul

echo [2/3] Starting Backend Agent...
start "Backend Agent" cmd /k "cd backend && .\run.bat"
timeout /t 5 /nobreak >nul

echo [3/3] Starting Frontend...
start "Frontend" cmd /k "cd frontend && pnpm dev"

echo.
echo ========================================
echo All services started successfully!
echo ========================================
echo.
echo LiveKit Server: ws://127.0.0.1:7880
echo Frontend URL:   http://localhost:3000
echo.
echo Close the terminal windows to stop services.
echo Press any key to exit this window...
pause >nul
