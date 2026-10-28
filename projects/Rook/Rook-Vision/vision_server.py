"""Runs on the PC that has the Pixy AND LM Studio (the 2nd PC).

Rook on the main PC sends it a question over your home network; this takes the
photo, asks LM Studio on the SAME PC (localhost), and sends back only text.
No picture ever crosses the network.

  python vision_server.py            (or double-click Start_Vision_Server.bat)
  python vision_server.py --port 8765

Test from any PC:  http://<2nd PC IP>:8765/health   (shows LM Studio models)
Settings in config.json: server_port (8765), server_token ("" = none).
LAN only: do not port-forward this on your router.
"""
import argparse
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from common import load_config, grab_frame, save_frame
from vision_client import ask_image, list_models, OBJECT_QUESTION, OBJECT_SYSTEM

CFG = load_config()
LOCK = threading.Lock()  # one camera, one question at a time


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(time.strftime("%H:%M:%S"), self.address_string(), fmt % args, flush=True)

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
        if self.path != "/health":
            return self._send(404, {"error": "not found"})
        if not self._authorized():
            return self._send(401, {"error": "bad token"})
        try:
            models = list_models(CFG)
            self._send(200, {"ok": True, "camera_index": CFG["camera_index"], "models": models})
        except Exception as e:
            self._send(200, {"ok": False, "error": f"LM Studio not reachable on this PC: {e}"})

    def do_POST(self):
        if self.path != "/look":
            return self._send(404, {"error": "not found"})
        if not self._authorized():
            return self._send(401, {"error": "bad token"})
        try:
            n = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(n) or b"{}")
            question = (body.get("question") or "").strip()
            mode = body.get("mode")
            question = question or "Describe what you see in one to three sentences."
            with LOCK:
                t0 = time.time()
                frame = grab_frame(CFG)
                t_cam = time.time() - t0
                if CFG.get("keep_snapshots_from_rook"):
                    save_frame(frame, CFG)
                if mode == "object":   # workshop mode: structured object description, longer answer allowed
                    answer, t_model = ask_image(CFG, frame, OBJECT_QUESTION, system=OBJECT_SYSTEM,
                                                max_tokens=CFG.get("object_max_tokens", 260))
                else:
                    answer, t_model = ask_image(CFG, frame, question)
            self._send(200, {"answer": answer, "t_cam": round(t_cam, 2), "t_model": round(t_model, 2)})
        except Exception as e:
            self._send(500, {"error": str(e)})


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=CFG.get("server_port", 8765))
    a = p.parse_args()
    srv = ThreadingHTTPServer(("0.0.0.0", a.port), Handler)
    print(f"Rook vision server on port {a.port}. Camera index {CFG['camera_index']}, "
          f"LM Studio at {CFG['server_url']}. Ctrl+C to stop.", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
