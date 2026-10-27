"""Light, no-AI-model check: is a face looking at the camera? Uses the Haar
cascade that ships inside OpenCV, so nothing extra to download. It is a cheap
gate: only wake the big vision model when this says someone is there.

  python presence.py            (checks once a second, Ctrl+C to stop)
"""
import time

import cv2

from common import load_config, open_camera

_cascade = None


def _get_cascade():
    global _cascade
    if _cascade is None:
        path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        _cascade = cv2.CascadeClassifier(path)
    return _cascade


def faces_in(frame):
    small = cv2.resize(frame, (640, int(640 * frame.shape[0] / frame.shape[1])))
    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    found = _get_cascade().detectMultiScale(gray, scaleFactor=1.15, minNeighbors=5, minSize=(60, 60))
    return len(found)


def main():
    cfg = load_config()
    cap = open_camera(cfg, width=1280, height=720)
    print("Watching for a face. Ctrl+C to stop.")
    last = None
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                time.sleep(0.2)
                continue
            n = faces_in(frame)
            state = n > 0
            if state != last:
                print(time.strftime("%H:%M:%S"), "face seen" if state else "nobody in view")
                last = state
            time.sleep(1.0)
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()


if __name__ == "__main__":
    main()
