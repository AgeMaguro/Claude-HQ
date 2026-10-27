"""Config loader with no OpenCV import, so remote mode never needs cv2 on the main PC."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load_config():
    with open(os.path.join(HERE, "config.json"), "r", encoding="utf-8") as f:
        return json.load(f)
