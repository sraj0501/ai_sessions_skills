@echo off
rem Windows post-tool-use hook shim: hands the harness's payload (stdin) to
rem capture.py. Works from cmd.exe and PowerShell, and tolerates paths with
rem spaces. All logic lives in Python.
rem
rem   hook-capture.cmd [harness-name]
setlocal
set "HARNESS=%~1"
if "%HARNESS%"=="" set "HARNESS=%AI_SKILLS_HARNESS%"
if "%HARNESS%"=="" set "HARNESS=unknown"
where py >nul 2>nul && (
  py -3 "%~dp0capture.py" --harness "%HARNESS%" 2>nul
  exit /b 0
)
where python3 >nul 2>nul && (
  python3 "%~dp0capture.py" --harness "%HARNESS%" 2>nul
  exit /b 0
)
where python >nul 2>nul && (
  python "%~dp0capture.py" --harness "%HARNESS%" 2>nul
  exit /b 0
)
exit /b 0
