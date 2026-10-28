@echo off
rem Run ONCE on the 2nd PC (double-click). Starts the launcher now and at every login, with no window.
cd /d "%~dp0"
set "PYW=%~dp0venv\Scripts\pythonw.exe"
if not exist "%PYW%" (
  echo Could not find venv\Scripts\pythonw.exe. Run setup.bat first.
  pause
  exit /b 1
)
powershell -NoProfile -Command "$s=(New-Object -ComObject WScript.Shell).CreateShortcut([Environment]::GetFolderPath('Startup')+'\RookVisionLauncher.lnk'); $s.TargetPath='%PYW%'; $s.Arguments='vision_launcher.py'; $s.WorkingDirectory='%~dp0'; $s.WindowStyle=7; $s.Save()"
start "" "%PYW%" vision_launcher.py
echo.
echo Launcher installed and running. Also run Open_Firewall.bat as administrator once (it now opens port 8766 too).
pause
