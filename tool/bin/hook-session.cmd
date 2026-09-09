@echo off
rem Windows session-lifecycle hook shim. Returns immediately and prints
rem nothing. All logic lives in session.py.
rem
rem   hook-session.cmd start|end [harness-name]
setlocal
set "ACTION=hook-start"
if /i "%~1"=="end" set "ACTION=hook-end"
if /i "%~1"=="hook-end" set "ACTION=hook-end"
set "HARNESS=%~2"
if "%HARNESS%"=="" set "HARNESS=%AI_SKILLS_HARNESS%"
if "%HARNESS%"=="" set "HARNESS=unknown"
set "SCRIPT=%~dp0session.py"

where py.exe >nul 2>nul
if not errorlevel 1 py -3 "%SCRIPT%" "%ACTION%" "%HARNESS%" 2>nul
if not errorlevel 1 exit /b 0

where python3.exe >nul 2>nul
if not errorlevel 1 python3 "%SCRIPT%" "%ACTION%" "%HARNESS%" 2>nul
if not errorlevel 1 exit /b 0

where python.exe >nul 2>nul
if not errorlevel 1 python "%SCRIPT%" "%ACTION%" "%HARNESS%" 2>nul
exit /b 0
