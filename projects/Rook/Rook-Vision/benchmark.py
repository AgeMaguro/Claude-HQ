"""Stage 3: compare vision models on the SAME photo.

  python capture_frame.py                      (take a test photo first, ideally with
                                                you holding a small printed label)
  python benchmark.py snapshots\\frame_XXXX.jpg --models qwen3-vl-8b gemma-3-12b
  python benchmark.py snapshots\\frame_XXXX.jpg      (tries every model the server lists)

LM Studio loads each model on first use, so the first answer from each model is
slower. Time the SECOND run if you want speed numbers. Results are saved in results\\.
"""
import argparse
import os
import time

from common import HERE, load_config, fail
from vision_client import ask_image, list_models

QUESTIONS = [
    "Is there a person in the photo? Describe them and what they are doing.",
    "What objects are on the desk?",
    "Read any text you can see, exactly as written.",
]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("image")
    p.add_argument("--models", nargs="*")
    p.add_argument("--server")
    a = p.parse_args()
    cfg = load_config()
    if a.server:
        cfg["server_url"] = a.server

    try:
        models = a.models or list_models(cfg)
    except Exception as e:
        fail(f"Could not list models: {e}")
    models = [m for m in models if "embed" not in m.lower()]

    lines = [f"# Vision benchmark {time.strftime('%Y-%m-%d %H:%M')}", f"Image: {a.image}",
             f"Server: {cfg['server_url']}", f"Max image side: {cfg['max_image_side']}", ""]
    for m in models:
        lines.append(f"## {m}")
        print(f"\n=== {m} ===")
        for q in QUESTIONS:
            try:
                ans, secs = ask_image(cfg, a.image, q, model=m)
            except Exception as e:
                ans, secs = f"ERROR: {e}", 0.0
            print(f"[{secs:5.1f}s] {q}\n   -> {ans}")
            lines += [f"- **Q:** {q}", f"  - **{secs:.1f}s:** {ans}"]
        lines.append("")
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    out = os.path.join(HERE, "results", time.strftime("benchmark_%Y%m%d_%H%M%S.md"))
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\nSaved", out)


if __name__ == "__main__":
    main()
