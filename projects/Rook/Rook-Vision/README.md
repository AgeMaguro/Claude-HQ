# Rook-Vision: let Rook see you (EMEET Pixy + local vision AI)

Goal: Rook can look through the EMEET Pixy and answer by voice ("Rook, can you see me?", "what am I holding?"), with everything staying on your own PCs. No frames leave your network.

Status: all code written and logic-tested against a fake server. NOT yet run with the real Pixy or LM Studio. Work through the stages in order; each one proves one piece.

## How it fits together
Pixy -> `capture_frame` (OpenCV, one photo on demand) -> `vision_client` (sends photo + question to LM Studio's local server) -> text answer -> Rook speaks it.
`vision.py` is the only file Rook will import later. Rook itself is not changed until stage 4.

## Stage 0: one-time setup (on the PC with the Pixy)
1. Double-click `setup.bat` (makes a `venv` here and installs OpenCV).
2. Open a terminal in this folder and run `venv\Scripts\activate`.
3. Close EMEET Studio, Zoom, Discord video, OBS: only one program can use the camera at a time.

## Stage 1: camera works
- `python list_cameras.py` shows camera names and which index works. Put the Pixy's number in `config.json` (`camera_index`).
- `python capture_frame.py --preview` shows a live window (Q quits, S saves).
- `python capture_frame.py` saves one 1080p photo into `snapshots\`. Try `--width 3840 --height 2160` for 4K.
Pass: you get a sharp photo of you at your desk.

## Stage 2: a vision model answers
1. In LM Studio, download a vision model. The model card shows an eye icon for vision support. Good starters for 8 GB of VRAM: Qwen3-VL 8B, Qwen2.5-VL 7B, Gemma 3 12B (all Q4).
2. LM Studio, Developer tab: load the model and start the server (default port 1234).
3. Test with a saved photo first: `python ask.py "What do you see?" --image snapshots\<file>.jpg`
4. Then live: `python ask.py "Can you see me? What am I doing?"`
If LM Studio runs on the GTX 1080 PC: turn on "Serve on Local Network", then either edit `server_url` in `config.json` to `http://<that PC's IP>:1234/v1` or use `--server`.
Pass: sensible answer in a few seconds.

## Stage 3: pick the model
Take one photo with you holding something with small printed text, then
`python benchmark.py snapshots\<file>.jpg --models <id1> <id2>` (ids come from `python ask.py --models`). It asks each model the same three questions, times them, and writes a report to `results\`. First answer per model is slow because LM Studio loads it.
Optional: `python presence.py` checks once a second whether a face is in view, using OpenCV only (no AI model). Useful later as a cheap gate before waking the big model.

## Stage 4: hook into Rook (later session, not done)
Back up the Rook folder first, then add a small call in Rook's command handling: `import vision` and `reply = vision.handle(text)`; speak it if not None. Triggers are in `vision.py` (`TRIGGERS`). Add a short numbered "Things to test" list when done.

## Notes
- Privacy: the Pixy's status LED is not wired to the sensor (reported in a Windows Central review), so it could be recording with no light. This project opens the camera only for about a second per question, then releases it. Keep the Pixy's privacy mode on when you are not using it.
- Pixy specs (from reviews): 4K at 30 fps or 1080p at 60 fps, plugs in over USB-C, works as a standard UVC webcam. Scripts ask for MJPG, which those modes need.
- Gimbal and AI auto-tracking are described as EMEET Studio features. I have not assumed scripts can steer the gimbal. If Studio is running it may hold the camera; close it for these scripts. If tracking is on while you test, the camera may move to follow you, which is fine.
- 4K is optional. Photos are shrunk to `max_image_side` (1024) before sending. Raise it to 1536 or 2048 if small text is not read well, at the cost of speed.
- Skip the Pixy's own mic; keep using the headset.
- Face recognition (knowing WHO you are) is not included. Possible later; it would store face data, so decide that deliberately.

## Stage 5: camera + LM Studio on the 2nd PC (added 2026-10-27, not yet tested on real hardware)
The Pixy is plugged into the 2nd PC (GTX 1080). That PC runs LM Studio AND `vision_server.py`. Rook on the main PC asks it over your home network and gets back text only; no photo crosses the network.

On the 2nd PC (one time):
1. Copy this whole `Rook-Vision` folder to it (skip `venv`, `snapshots`, `__pycache__`). Double-click `setup.bat`.
2. `venv\Scripts\python list_cameras.py`; put the Pixy's number in `config.json` as `camera_index` (close EMEET Studio first). Leave `remote_url` empty on this PC.
3. Install LM Studio, download a vision model (Qwen3-VL 8B or 4B, Q4), Developer tab: load it and start the server. `server_url` stays `http://localhost:1234/v1`. Turn "never unload" on.
4. Run `Open_Firewall.bat` once as administrator (network must be set to Private).
5. Double-click `Start_Vision_Server.bat` and leave the window open. Note the PC's IP (`ipconfig`).
Test from the main PC browser: `http://<2nd PC IP>:8765/health` should show `"ok": true` and the model name.

On the main PC: in `config.json` set `"remote_url": "http://<2nd PC IP>:8765"`. Rook's existing `rook_eyes.py` / `look.py` then use the 2nd PC automatically. Set `"remote_url": ""` to go back to the local camera. Optional `server_token` (same value in both configs) if you want a password.
