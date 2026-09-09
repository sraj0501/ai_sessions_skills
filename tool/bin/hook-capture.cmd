@echo off
rem Windows post-tool-use hook shim: hands the harness's payload (stdin) to
rem capture.py. Deliberately avoids labels and parenthesised blocks so it is
rem robust regardless of line endings, and quotes %~dp0 so a tool path with
rem spaces still works. All logic lives in Python.
rem
rem   hook-capture.cmd [harness-name]
setlocal
set "HARNESS=%~1"
if "%HARNESS%"=="" set "HARNESS=%AI_SKILLS_HARNESS%"
if "%HARNESS%"=="" set "HARNESS=unknown"
set "SCRIPT=%~dp0capture.py"

where py.exe >nul 2>nul
if not errorlevel 1 py -3 "%SCRIPT%" --harness "%HARNESS%" 2>nul
if not errorlevel 1 exit /b 0

where python3.exe >nul 2>nul
if not errorlevel 1 python3 "%SCRIPT%" --harness "%HARNESS%" 2>nul
if not errorlevel 1 exit /b 0

where python.exe >nul 2>nul
if not errorlevel 1 python "%SCRIPT%" --harness "%HARNESS%" 2>nul
exit /b 0
