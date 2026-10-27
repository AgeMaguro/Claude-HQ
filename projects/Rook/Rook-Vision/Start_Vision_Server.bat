@echo off
cd /d "%~dp0"

rem Start LM Studio's server and load the vision model first, so the first "can you see me" is not slow.
rem If lms is not on PATH it is usually in %USERPROFILE%\.lmstudio\bin (run "lms bootstrap" there once).
rem If these two lines fail, the vision server below still starts; check "lms load --help" for flags.
rem Keep the model id in sync with "model" in config.json.
set "LMS=lms"
where lms >nul 2>nul || set "LMS=%USERPROFILE%\.lmstudio\bin\lms.exe"
"%LMS%" server start
"%LMS%" load qwen/qwen3-vl-8b --gpu max --context-length 8192 -y

venv\Scripts\python.exe vision_server.py
pause
