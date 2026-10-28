"""Tiny always-on helper for the 2nd PC (the one with the Pixy and LM Studio).

Rook on the main PC asks it to start Start_Vision_Server.bat when the vision server
is not running. It can start that one batch file and nothing else.

  venv\\Scripts\\pythonw.exe vision_launcher.py   (no window; Install_Launcher_Startup.bat sets this up at login)
  venv\\Scripts\\python.exe vision_launcher.py    (with a window, for testing)

  GET  /status  -> {"launcher": true, "server_up": true/false}
  POST /start   -> starts Start_Vision_Server.bat unless the server is already up or was just started
  POST /stop    -> stops the vision server (and its window) and unloads the model from LM Studio to free the GPU

Settings in config.json (all optional): launcher_port (8766), server_port (8765), server_token ("" = none;
the same token as the vision server, sent as the X-Rook-Token header).
LAN only: do not port-forward this on your router. Log: launcher_log.txt next to this file.
"""
import json
import os
import subprocess
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from common_light import HERE, load_config

CFG = load_config()
PORT = int(CFG.get("launcher_port", 8766))
SERVER_PORT = int(CFG.get("server_port", 8765))
COOLDOWN_SECONDS = 60   # after a start, don't start a second copy while the first is still loading
LOCK = threading.Lock()
STATE = {"last_start": 0.0, "pid": None}
LOG = os.path.join(HERE, "launcher_log.txt")


def log(text):
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + text + "\n")
    except Exception:
        pass


def server_up():
    """True if anything answers on the vision server's port (even an error reply means it is running)."""
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{SERVER_PORT}/health", timeout=2):
            return True
    except urllib.error.HTTPError:
        return True
    except Exception:
        return False


def start_server():
    flags = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)  # own window, like double-clicking the .bat
    p = subprocess.Popen(["cmd", "/c", os.path.join(HERE, "Start_Vision_Server.bat")], cwd=HERE, creationflags=flags)
    STATE["pid"] = p.pid


def _run(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=30,
                              creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    except Exception as e:
        log(f"command failed {cmd[0]}: {e}")
        return None


def stop_server():
    """Kill the server's window/process tree, then anything still listening on the server port, then unload LM Studio models."""
    if STATE["pid"]:
        _run(["taskkill", "/PID", str(STATE["pid"]), "/T", "/F"])   # the cmd window we opened and the python under it
        STATE["pid"] = None
    # a server started by hand (or the window was already gone): kill whatever owns the port
    _run(["powershell", "-NoProfile", "-Command",
          f"Get-NetTCPConnection -LocalPort {SERVER_PORT} -State Listen -ErrorAction SilentlyContinue | "
          "ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }"])
    lms = "lms"
    if _run(["where", "lms"]) is None or _run(["where", "lms"]).returncode != 0:
        lms = os.path.join(os.path.expanduser("~"), ".lmstudio", "bin", "lms.exe")
    _run([lms, "unload", "--all"])
    log("stopped vision server and unloaded models")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        log(f"{self.address_string()} {fmt % args}")

    def _send(self, code, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _authorized(self):
        token = CFG.get("server_token", "")
        return (not token) or self.headers.get("X-Rook-Token", "") == token

    def do_GET(self):
        if self.path != "/status":
            return self._send(404, {"error": "not found"})
        if not self._authorized():
            return self._send(401, {"error": "bad token"})
        self._send(200, {"launcher": True, "server_up": server_up()})

    def do_POST(self):
        if self.path not in ("/start", "/stop"):
            return self._send(404, {"error": "not found"})
        if not self._authorized():
            return self._send(401, {"error": "bad token"})
        if self.path == "/stop":
            with LOCK:
                stop_server()
                STATE["last_start"] = 0.0
            return self._send(200, {"stopped": True})
        with LOCK:
            if server_up():
                return self._send(200, {"started": False, "already_running": True})
            if time.time() - STATE["last_start"] < COOLDOWN_SECONDS:
                return self._send(200, {"started": False, "starting": True})
            try:
                start_server()
                STATE["last_start"] = time.time()
                log("started Start_Vision_Server.bat")
                return self._send(200, {"started": True})
            except Exception as e:
                log(f"start failed: {e}")
                return self._send(500, {"error": f"could not start the vision server: {e}"})


if __name__ == "__main__":
    log(f"launcher listening on port {PORT}")
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
