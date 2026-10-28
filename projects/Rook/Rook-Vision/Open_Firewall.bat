@echo off
rem Right-click > Run as administrator, ONCE, on the 2nd PC. Lets the main PC reach port 8765 (vision server) and 8766 (launcher) on your home network only.
netsh advfirewall firewall add rule name="Rook Vision Server" dir=in action=allow protocol=TCP localport=8765 profile=private
netsh advfirewall firewall add rule name="Rook Vision Launcher" dir=in action=allow protocol=TCP localport=8766 profile=private
pause
