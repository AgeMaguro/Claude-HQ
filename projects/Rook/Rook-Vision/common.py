"""Shared helpers: config loading and camera opening for Rook-Vision."""
import json
import os
import sys
import time

import cv2

HERE = os.path.dirname(os.path.abspath(__file__))


def load_config():
    with open(os.path.join(HERE, "config.json"), "r", encoding="utf-8") as f:
        return json.load(f)


def _backend(name):
    name = (name or "").lower()
    if name == "dshow":
        return cv2.CAP_DSHOW
    if name == "msmf":
        return cv2.CAP_MSMF
    return cv2.CAP_ANY


def open_camera(cfg, index=None, width=None, height=None):
    """Open the camera. Asks for MJPG, which 1080p60 and 4K need over USB 2.0."""
    index = cfg["camera_index"] if index is None else index
    width = cfg["width"] if width is None else width
    height = cfg["height"] if height is None else height
    cap = cv2.VideoCapture(index, _backend(cfg.get("backend")))
    if not cap.isOpened():
        raise RuntimeError(
            f"Could not open camera {index}. Close EMEET Studio, Zoom, Discord "
            "and anything else using it, then try again (or run list_cameras.py)."
        )
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FPS, cfg.get("fps", 30))
    return cap


def grab_frame(cfg, index=None, width=None, height=None):
    """Open the camera, let auto exposure/focus settle, grab one frame, release.

    The camera is only open for about a second, then released. That is on
    purpose: the Pixy's LED is not wired to the sensor, so we never leave it
    running in the background.
    """
    cap = open_camera(cfg, index, width, height)
    try:
        frame = None
        for _ in range(max(1, cfg.get("warmup_frames", 15))):
            ok, f = cap.read()
            if ok:
                frame = f
            else:
                time.sleep(0.03)
        if frame is None:
            raise RuntimeError("Camera opened but gave no frames.")
        return frame
    finally:
        cap.release()


def save_frame(frame, cfg, name=None):
    folder = os.path.join(HERE, cfg.get("snapshots_dir", "snapshots"))
    os.makedirs(folder, exist_ok=True)
    name = name or time.strftime("frame_%Y%m%d_%H%M%S.jpg")
    path = os.path.join(folder, name)
    cv2.imwrite(path, frame, [cv2.IMWRITE_JPEG_QUALITY, int(cfg.get("jpeg_quality", 90))])
    return path


def fail(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)
