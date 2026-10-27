"""Stage 2: take a photo with the Pixy and ask the local vision model about it.

  python ask.py "What am I holding?"
  python ask.py "Can you see me? What am I doing?"
  python ask.py "Read the label" --image snapshots\\some_frame.jpg   (skip the camera)
  python ask.py --models                                               (list models on the server)
"""
import argparse

from common import load_config, grab_frame, save_frame, fail
from vision_client import ask_image, list_models


def main():
    p = argparse.ArgumentParser()
    p.add_argument("question", nargs="?", default="Describe what you see. Is there a person? What are they doing?")
    p.add_argument("--image", help="use a saved image instead of the camera")
    p.add_argument("--model", help="override config model id")
    p.add_argument("--models", action="store_true", help="list models the server offers")
    p.add_argument("--server", help="override server_url, e.g. http://192.168.1.50:1234/v1")
    a = p.parse_args()

    cfg = load_config()
    if a.server:
        cfg["server_url"] = a.server

    try:
        if a.models:
            for m in list_models(cfg):
                print(m)
            return
        if a.image:
            image = a.image
        else:
            frame = grab_frame(cfg)
            print("Photo saved:", save_frame(frame, cfg))
            image = frame
        answer, secs = ask_image(cfg, image, a.question, model=a.model)
    except Exception as e:
        fail(f"Problem: {e}")

    print(f"\nAnswer ({secs:.1f}s): {answer}")


if __name__ == "__main__":
    main()
