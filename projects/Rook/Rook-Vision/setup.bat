@echo off
rem One-time setup: makes a venv in this folder and installs the packages.
cd /d "%~dp0"
if not exist venv (
  py -3.11 -m venv venv || python -m venv venv
)
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.
echo Done. Next: run  venv\Scripts\activate  then  python list_cameras.py
pause
