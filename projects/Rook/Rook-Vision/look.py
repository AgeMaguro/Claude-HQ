"""Command-line door for Rook: python look.py "question"  -> prints ONLY the spoken answer.

Rook runs this with Rook-Vision's own venv, so Rook's Python never needs OpenCV.
Exit code 0 = answer printed. 1 = problem (the message is printed instead).

Two modes (config.json):
  remote_url = ""                    camera and LM Studio are on THIS PC (original mode)
  remote_url = "http://<IP>:8765"    camera and LM Studio are on the 2nd PC, which runs
                                     vision_server.py; only text crosses the network
"""
import json
import sys
import time
import urllib.error
import urllib.request

from common_light import load_config


def look_remote(cfg, question, mode=None):
    url = cfg["remote_url"].rstrip("/") + "/look"
    headers = {"Content-Type": "application/json"}
    if cfg.get("server_token"):
        headers["X-Rook-Token"] = cfg["server_token"]
    req = urllib.request.Request(url, data=json.dumps({"question": question, "mode": mode}).encode("utf-8"), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=cfg.get("timeout_s", 180) + 30) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            msg = json.loads(e.read().decode("utf-8")).get("error", "")
        except Exception:
            msg = ""
        raise RuntimeError(msg or f"The vision PC returned error {e.code}.")
    except urllib.error.URLError as e:
        raise RuntimeError(
            f"Could not reach the vision PC at {cfg['remote_url']} ({e.reason}). Is it on, "
            "and is Start_Vision_Server.bat running there?"
        )
    print(f"timing: remote camera {data.get('t_cam', 0):.1f}s, model {data.get('t_model', 0):.1f}s",
          file=sys.stderr)
    return data["answer"]


def look_local(cfg, question, mode=None):
    from common import grab_frame, save_frame
    from vision_client import ask_image, OBJECT_QUESTION, OBJECT_SYSTEM
    t0 = time.time()
    frame = grab_frame(cfg)
    t_cam = time.time() - t0
    if cfg.get("keep_snapshots_from_rook"):
        save_frame(frame, cfg)
    if mode == "object":
        answer, t_model = ask_image(cfg, frame, OBJECT_QUESTION, system=OBJECT_SYSTEM,
                                    max_tokens=cfg.get("object_max_tokens", 160))
    else:
        answer, t_model = ask_image(cfg, frame, question)
    print(f"timing: camera {t_cam:.1f}s, model {t_model:.1f}s", file=sys.stderr)
    return answer


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    args = sys.argv[1:]
    mode = None
    if args and args[0] == "--object":   # workshop mode: describe and size the held object
        mode, args = "object", args[1:]
    question = " ".join(args).strip() or "Describe what you see in one to three sentences."
    cfg = load_config()
    try:
        answer = look_remote(cfg, question, mode) if cfg.get("remote_url") else look_local(cfg, question, mode)
    except Exception as e:
        print(str(e))
        sys.exit(1)
    print(answer)


if __name__ == "__main__":
    main()
