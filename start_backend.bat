@echo off
title BharatProblemBase
cd /d "%~dp0"

echo Building frontend...
cd frontend
call npm run build
cd ..

echo.
echo Starting BharatProblemBase...
echo Open http://localhost:8000 in your browser
echo.

if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000
) else (
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
)
pause
