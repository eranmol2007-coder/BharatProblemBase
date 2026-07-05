@echo off
echo Stopping BharatProblemBase server on port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    taskkill /F /PID %%a >nul 2>&1
)
echo Server stopped successfully.
pause
