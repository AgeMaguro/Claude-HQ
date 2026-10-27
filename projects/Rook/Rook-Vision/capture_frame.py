"""Stage 1b: save one frame from the Pixy.

  python capture_frame.py                 (uses config.json: 1920x1080)
  python capture_frame.py --width 3840 --height 2160
  python capture_frame.py --preview       (live window; press Q to quit, S to save)
"""
import argparse

import cv2

from common import load_config, grab_frame, save_frame, open_camera


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--index", type=int)
    p.add_argument("--width", type=int)
    p.add_argument("--height", type=int)
    p.add_argument("--preview", action="store_true")
    a = p.parse_args()
    cfg = load_config()

    if a.preview:
        cap = open_camera(cfg, a.index, a.width, a.height)
        print("Preview open. Q = quit, S = save a frame.")
        try:
            while True:
                ok, frame = cap.read()
                if not ok:
                    continue
                small = cv2.resize(frame, (960, int(960 * frame.shape[0] / frame.shape[1])))
                cv2.imshow("Pixy preview", small)
                k = cv2.waitKey(1) & 0xFF
                if k in (ord("q"), 27):
                    break
                if k == ord("s"):
                    print("Saved", save_frame(frame, cfg))
        finally:
            cap.release()
            cv2.destroyAllWindows()
        return

    frame = grab_frame(cfg, a.index, a.width, a.height)
    h, w = frame.shape[:2]
    path = save_frame(frame, cfg)
    print(f"Saved {w}x{h} frame: {path}")


if __name__ == "__main__":
    main()
