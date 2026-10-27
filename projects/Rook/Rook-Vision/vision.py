"""Stage 4: the one file Rook imports. Nothing here knows about Rook's internals.

Hook-up (a later session, after the stages above pass):
    import vision
    reply = vision.handle(spoken_text)     # None if it is not a vision request
    if reply: speak(reply)

The camera is opened only while taking the photo, then released.
"""
import re

from common import load_config, grab_frame, save_frame
from vision_client import ask_image

# Spoken triggers -> the question sent to the model. First match wins.
TRIGGERS = [
    (r"\b(can you see me|do you see me|am i (there|in view|visible))\b",
     "Is there a person in the photo? If yes, say what they look like and what they are doing."),
    (r"\b(what am i holding|what is this|what's this|look at this)\b",
     "What is the main object the person is holding or pointing at? Name it and describe it briefly."),
    (r"\bread (this|that|the label|the text)\b",
     "Read the text you can see, exactly as written."),
    (r"\b(what do you see|look at the (desk|printer|screen)|take a look)\b",
     "Describe what you see in one to three sentences."),
]


def look(question):
    """Take a photo and answer a question about it. Returns text to speak."""
    cfg = load_config()
    try:
        frame = grab_frame(cfg)
        if cfg.get("keep_snapshots_from_rook"):
            save_frame(frame, cfg)
        answer, _ = ask_image(cfg, frame, question)
        return answer
    except Exception as e:
        return f"I could not look just now. {e}"


def handle(spoken_text):
    """Return a reply if the text is a vision request, else None."""
    t = (spoken_text or "").lower()
    for pattern, question in TRIGGERS:
        if re.search(pattern, t):
            return look(question)
    return None


if __name__ == "__main__":
    import sys
    text = " ".join(sys.argv[1:]) or "what do you see"
    print(handle(text) or "(not a vision request)")
