@echo off
title BharatProblemBase
cd /d "%~dp0"

echo Building frontend...
cd frontend
call npm run build
cd ..

echo Starting BharatProblemBase Backend...
start /min "BharatProblemBase" cmd /c ".venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

echo Waiting for server...
timeout /t 5 /nobreak >nul

echo Opening website...
start http://localhost:8000
echo.
echo Website is now running at http://localhost:8000
echo You can close this window - the server runs in the background.
pause
