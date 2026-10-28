"""Talks to a local vision model through LM Studio's OpenAI-compatible server.

Only the standard library plus OpenCV is used. Nothing leaves your network:
server_url is localhost, or the LAN address of the GTX 1080 PC.
"""
import base64
import json
import time
import urllib.error
import urllib.request

import cv2

DEFAULT_SYSTEM = (
    "You are the eyes of a desktop voice assistant named Rook. You are given one "
    "photo from a webcam on the user's desk. Answer the question briefly and "
    "plainly, in one short sentence (about 20 words) unless asked to read text, as "
    "it will be spoken aloud. Say only what you can actually see. If something is "
    "unclear or too small to read, say so."
)


def image_to_data_url(image, max_side=1024, quality=90):
    """image: OpenCV frame (numpy array) or a path to an image file."""
    if isinstance(image, str):
        frame = cv2.imread(image)
        if frame is None:
            raise FileNotFoundError(f"Could not read image: {image}")
    else:
        frame = image
    h, w = frame.shape[:2]
    scale = max_side / max(h, w)
    if scale < 1:
        frame = cv2.resize(frame, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
    ok, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
    if not ok:
        raise RuntimeError("Could not encode image.")
    return "data:image/jpeg;base64," + base64.b64encode(buf.tobytes()).decode("ascii")


def _post(url, payload, timeout):
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def list_models(cfg):
    url = cfg["server_url"].rstrip("/") + "/models"
    with urllib.request.urlopen(url, timeout=10) as r:
        data = json.loads(r.read().decode("utf-8"))
    return [m["id"] for m in data.get("data", [])]


# Used by workshop mode ("scan what I'm holding"): a short structured description plus a size estimate.
OBJECT_QUESTION = "Describe the object being held, using the required format."
OBJECT_SYSTEM = (
    "You help a 3D-printing assistant. You are given one webcam photo of a person holding one object. "
    "Ignore the person, their hands, and the background; describe only the held object in enough detail to model it. "
    "Reply in exactly these lines and nothing else:\n"
    "OBJECT: what it is, a few words\n"
    "PARTS: the main parts from top to bottom or front to back, each with its shape and rough proportion, "
    "e.g. 'head: round, 1/3 of height; ears: two pointed triangles; body: tapered cylinder; base: flat oval plate'. Up to 6 parts.\n"
    "FEATURES: distinctive 3D details worth modelling (pose, handles, holes, ridges, raised or recessed shapes, curves). "
    "Ignore colors and flat printed patterns.\n"
    "SIZE_MM: width x depth x height in millimeters, ONE best estimate, no ranges. Height is the vertical size as the object "
    "normally stands or sits. Use the hand as the scale: an adult palm is about 85 mm wide and a finger about 18 mm wide. "
    "Objects held in one hand are rarely over 200 mm.\n"
    "CONFIDENCE: low, medium or high\n"
    "If no object is being held, reply with only: NONE"
)


def ask_image(cfg, image, question, model=None, system=DEFAULT_SYSTEM, max_tokens=None):
    """Returns (answer_text, seconds). Raises RuntimeError with a plain message."""
    data_url = image_to_data_url(image, cfg.get("max_image_side", 1024), cfg.get("jpeg_quality", 90))
    payload = {
        "model": model or cfg.get("model") or "",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": [
                {"type": "text", "text": question},
                {"type": "image_url", "image_url": {"url": data_url}},
            ]},
        ],
        # Each generated token costs ~0.1 s on the GTX 1080, so cap the answer. Override with "max_answer_tokens" in config.json.
        "max_tokens": max_tokens or cfg.get("max_answer_tokens", 80),
        "temperature": 0.2,
    }
    url = cfg["server_url"].rstrip("/") + "/chat/completions"
    t0 = time.time()
    try:
        resp = _post(url, payload, cfg.get("timeout_s", 180))
    except urllib.error.URLError as e:
        raise RuntimeError(
            f"Could not reach the vision server at {cfg['server_url']} ({e.reason}). "
            "In LM Studio: Developer tab > start the server, load a vision model "
            "(look for the eye icon), and on another PC turn on 'Serve on Local Network'."
        )
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:300]
        raise RuntimeError(f"Vision server error {e.code}: {body}")
    text = resp["choices"][0]["message"]["content"].strip()
    return text, time.time() - t0
