@echo off
rem Windows session-lifecycle hook shim.
rem
rem   hook-session.cmd start|end [harness-name]
rem
rem Returns immediately and prints nothing. All logic lives in session.py.
setlocal
set "ACTION=%~1"
if "%ACTION%"=="" set "ACTION=start"
set "HARNESS=%~2"
if "%HARNESS%"=="" set "HARNESS=%AI_SKILLS_HARNESS%"
if "%HARNESS%"=="" set "HARNESS=unknown"
where py >nul 2>nul && (
  py -3 "%~dp0session.py" "%ACTION%" "%HARNESS%" 2>nul
  exit /b 0
)
where python3 >nul 2>nul && (
  python3 "%~dp0session.py" "%ACTION%" "%HARNESS%" 2>nul
  exit /b 0
)
where python >nul 2>nul && (
  python "%~dp0session.py" "%ACTION%" "%HARNESS%" 2>nul
  exit /b 0
)
exit /b 0
