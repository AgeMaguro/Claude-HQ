"""Stage 1a: find which camera index is the Pixy. Run: python list_cameras.py"""
import cv2

from common import load_config, _backend


def names():
    try:
        from pygrabber.dshow_graph import FilterGraph
        return FilterGraph().get_input_devices()
    except Exception:
        return []


def main():
    cfg = load_config()
    dev = names()
    if dev:
        print("Camera names Windows reports (index = position in this list):")
        for i, n in enumerate(dev):
            print(f"  {i}: {n}")
        print()
    print("Probing indexes 0-5 (this opens each camera for a moment):")
    for i in range(6):
        cap = cv2.VideoCapture(i, _backend(cfg.get("backend")))
        if cap.isOpened():
            ok, frame = cap.read()
            if ok:
                h, w = frame.shape[:2]
                print(f"  index {i}: works, default {w}x{h}")
            else:
                print(f"  index {i}: opens but no frame (busy, or a virtual camera)")
        cap.release()
    print("\nPut the Pixy's index in config.json as camera_index.")
    print("Note: the Pixy has a 2nd (AI tracking) sensor; it should still show as ONE camera.")


if __name__ == "__main__":
    main()
