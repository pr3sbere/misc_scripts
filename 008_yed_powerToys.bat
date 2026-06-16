
@echo off
echo Restarting Microsoft PowerToys...

:: Kill the PowerToys process
taskkill /f /im PowerToys.exe

:: Wait for a moment to ensure the process is terminated
timeout /t 2 /nobreak >nul

:: Start PowerToys from the default installation path
start "" "C:\Program Files\PowerToys\PowerToys.exe"

echo PowerToys has been restarted.
