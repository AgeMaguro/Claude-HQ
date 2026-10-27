# Rook handoff notes

Append dated sections at the bottom. Newest last.

## 2026-10-27 (DESKTOP-2) - Claude-HQ repo set up
Asked: set up handoff on the 2nd PC and make it shared across both PCs.
Done:
- Created this repo (Claude-HQ), START-HERE.md, Handoffs/ stubs, projects/ layout.
- Imported Rook-Vision source from DESKTOP-2 (projects/Rook/Rook-Vision). venv, snapshots, results, backups excluded.
- Rook-Vision README says stage 5 (camera + LM Studio on DESKTOP-2, vision_server.py on port 8765) is written but not tested on real hardware.
Open:
- The main PC's existing handoff notes (older Rook/TradeBot/Skills/Misc history) are NOT in the repo yet; a session on the main PC must merge them into Handoffs/ and push.
- Clone the repo into Desktop\Claude on both PCs (DESKTOP-2's folder currently holds Rook-Vision outside git).
- Update the user's Instructions-for-Claude setting to the new workflow (git pull first, push at end).
Things to test:
1. On DESKTOP-2: clone Claude-HQ, confirm START-HERE.md and Handoffs\ appear.
2. On the main PC: pull, then add old handoff history and push; confirm DESKTOP-2 sees it after a pull.
3. Rook-Vision stage 5 checks in its README (/health on port 8765).

## Imported history from the old Claude folder (merged 2026-10-27, main PC)

Everything below was copied word for word from the old `Claude\Handoffs\Rook.md` (that folder is now `claude-old` on the main PC), in its original order, oldest first. Paths inside these sections use the old layout; see START-HERE.md for where things live now.

Split out of `Claude_handoff.md` on 2026-10-12. Section text is copied word for word, in its original order (oldest first). The original file is kept in `Archive\`.

## Contents

1. Handoff: Rook voice assistant (session of 2026-10-09)
2. Handoff: Rook on Meta Quest 3 (planning chat, 2026-10-09 evening)
3. Handoff: Rook webcam / vision brainstorm (chat, 2026-10-10 evening)
4. Handoff: drones, 3D printing and Rook "workshop mode" (chat started 2026-10-09 around 3:20am US Central, notes updated 2026-10-11)
5. Handoff: Orbit menu sphere (chat, 2026-10-11 afternoon)
6. Handoff: Rook weather lookup for other towns (cloud session, 2026-10-11 about 4:15 to 4:55 pm US Central)
7. Handoff: Rook desktop skills (skills.py) and shutdown/restart fixes (2026-10-11 evening)
8. Handoff: Discord API for Rook, paused (chat, 2026-10-11 about 10:00 to 10:10 pm US Central)
9. Handoff: Rook-Vision, EMEET Pixy + local vision AI (chat, 2026-10-13 about 9:25 pm US Central)

---

<!-- source file: 2026-10-09_Rook-session-handoff.md -->

## Handoff: Rook voice assistant (session of 2026-10-09)

Written at the end of the session (about 2:49 pm US Central). Read this first, then the full notes in the Rook vault:
`C:\Users\cheye\Documents\GitHub\Rook-vault\Projects\Rook-handoff.md` (very detailed) and `Projects\Rook-bug-log.md`.

### Who and how to work with them
- Windows 10 PC, US Central time, beginner at scripting, Claude Pro (monthly) plan as of 2026-10-09. Calls the voice assistant "Rook" (second wake word "Ayah").
- Rook folder: `C:\Users\cheye\Desktop\Rook`. Vault (synced to private GitHub repo AgeMaguro/Rook-vault): `C:\Users\cheye\Documents\GitHub\Rook-vault`.
- Standing preference: end every update that changes Rook with a short numbered list of things to test.
- Wants new functionality in separate files, work in stages, backups before edits (`Rook\backups\`, about 80 files, 1.8 MB).
- "check now" from the user means: read `rook_last_report.txt`, `rook_debug_log.txt`, `rook_heard_log.txt` and the vault's `Daily\<date>.md`, then report what worked and what didn't.
- Privacy matters to them: keep everything local where possible; keep private details out of notes.

### What exists now (all in the Rook folder)
- `rook_mic.py` is the main program (start it with `Start_Rook_Mic.bat`). Mic + GPU Whisper + Kokoro voice + streaming replies + barge-in.
- `rook.py` is the brain: memory commands, tell-Claude, weather, clock answers, hardware answers.
- Workshop mode (`workshop_mode.py`, `workshop_cad.py`, `workshop_runner.py`): "Rook, workshop mode", then describe a part, then "make it" -> Claude writes a CadQuery script -> STL in `Rook\workshop\`. Tested with real CadQuery (a 40 x 25 x 10 mm box worked). Stage 3 (slicer + printer handoff, Flashforge Adventurer 5M, human in the loop, printer drops Wi-Fi) is NOT started; need the Orca-Flashforge install location.
- Conversation mode and follow-up window (`conversation_mode.py`): "Rook, conversation mode" / "talk to me" / "let's talk" (end with "that's all"); also 15 s after Rook answers, the next line needs no name. Tested and working.
- Hardware answers (`rook_hardware.py`): RAM, CPU, GPU, drive space, Windows version, specs. Tested and working.
- Shutdown family: "Rook, shut down", "Bye Rook", "Rook, restart" (needs `Start_Rook_Mic.bat`), "Rook, shut down and check" (types "check now" into the Claude desktop app after saving and syncing). Commands must be 7 words or fewer. A second Rook closes itself (`rook_single.py`).
- Logging: `rook_heard_log.txt` records every transcript and what Rook did with it (local only).

### Fixed today
Clock/date answers; ambient checks paused in workshop mode; long sentences that ended in "shut down Rook" no longer trigger shutdown; asks instead of assuming (Wordle test); a bug that dropped short first sentences from spoken replies (`take_sentences` in rook.py).

### Not yet confirmed by the user
- The clipped-speech fix (their last Rook run started before it was saved; the next run is the first with all changes).
- "Shut down and check" with the Claude app closed, and "restart and check".
- The "an NVIDIA" wording fix.

### Open ideas (do not start unless asked)
- Read-only PC abilities with an allowlist and a spoken yes for anything that changes the PC.
- Lower thinking effort for replies (Sonnet took 6 to 9 s on logic questions; user has not chosen).
- Private repo for the Rook code (only the vault is on GitHub; code backups are local only).
- Second audio source (Voicemeeter / loopback), private mode with a local model (LM Studio; GTX 1080 PC), phone app (Galaxy S26 Ultra), Discord late-audio issue, friend's wiki lookup.
- Console tip: clicking inside the Rook console window can freeze Rook until Enter/Esc (suspected cause of one 18 s pause).

### How sessions work (permissions are per session)
- Access to the Rook folder, vault, `Claude Handoff` folder and LM Studio models folder was granted this session; a new session needs fresh approval (use device_request_folder_access).
- Edit files on the PC through the device shell, `py_compile` them, and back up first. The cloud sandbox can't pip install or run the user's venv.
- Vault commits from the cloud clone (`/home/claude/rook-vault`): pull with `git fetch origin main` then `git pull --ff-only origin main`; end commits with the Co-Authored-By and Claude-Session lines.
- Work-time log: 2026-10-08 about 9:30 am to 4:58 pm (about 7.5 h). 2026-10-09 ended about 2:49 pm (start not recorded).

---

<!-- source file: 2026-10-09_Rook-Quest3-chat-handoff.md -->

## Handoff: Rook on Meta Quest 3 (planning chat, 2026-10-09 evening)

Companion to `2026-10-09_Rook-session-handoff.md` (read that first for how Rook is built and how to work with the user). Nothing on the PC was changed in this chat. It was planning only.

### The question
Can an app be built for the Meta Quest 3 that has Rook capabilities, and can it connect to what is already built?

### Answer given
Yes. Rook cannot run on the headset as it is (Python on Windows, GPU Whisper + Kokoro), so the Quest should be a front end that talks to the existing Rook on the PC.

Options discussed:
1. **Quest as a front end for the PC (recommended).** The headset does mic, speakers and display. A new, separate file on the PC runs a small local server. It takes audio from the Quest, runs the same Whisper -> `rook.py` -> Kokoro pipeline, and sends the reply back. The first client would be a simple web page opened in the Quest browser. `rook_mic.py` keeps working unchanged. Later idea: show workshop-mode STL files as 3D models in the room.
2. **Standalone Quest app (Unity / native Android).** Needs cloud or smaller on-headset speech models and costs quality and privacy. Talking to Claude directly needs a paid API key, separate from the free Claude plan. Much bigger project.
3. **Hybrid.** Start with option 1, add a cut-down standalone mode later.

### Caveats noted
- PC must be on and the Quest on the same Wi-Fi to start. Use from outside the home needs a VPN (later step).
- PC-only commands (e.g. "shut down and check", which types into the Claude desktop app) need limiting or disabling for Quest sessions.
- Server should be limited to the local network, with a simple access code.

### Not decided yet
The user has not said to go ahead. Open questions for them: voice only first, or the 3D STL viewer too?

### Suggested first step if they say go
Stage 1: a small test where the Quest sends one voice command and Rook answers it, to prove the connection. Back up the Rook folder first, put new code in new files, work in stages, and end any update that changes Rook with a short numbered list of things to test.

### Reminders
- A new session needs fresh folder approval (device_request_folder_access) for the Rook folder, vault and this handoff folder.
- Keep private details out of notes. Keep things local where possible.

---

<!-- source file: 2026-10-11_Rook-webcam-vision-handoff.md -->

## Handoff: Rook webcam / vision brainstorm (chat, 2026-10-10 evening)

Companion to `2026-10-09_Rook-session-handoff.md` (read that first for how Rook is built and how to work with the user). Nothing on the PC was changed in this chat. It was brainstorming only; the user's PC was off.

### The question
Could Rook be "trained" to recognize webcam input?

### Answer given
Yes, and no training is needed. Modern vision-language models already interpret images, so this is mostly plumbing: capture a frame, send it with the user's question to a vision model, have Rook speak the answer.

Options discussed:
1. **On-demand snapshot (recommended start).** A voice command ("Rook, look at this") grabs one frame with OpenCV and sends it plus the question to a vision model. Lives in its own file (e.g. `vision.py`) that `rook.py` references.
2. **Local vision model via LM Studio** (privacy). Candidates to test: Qwen2-VL (small), Gemma 3 (4B), a LLaVA variant. Roughly 3-8B quantized fits in 8 GB VRAM.
3. **Always-on / watch mode (later).** Lightweight local detection (OpenCV/YOLO) or low-rate frame sampling; only call the big model when something changes.

### Decisions from the user
- Keep it **local**. No frames leaving the PC.
- Test whether the vision model can run on the **second PC (GTX 1080, 8 GB)**.
- A **4K webcam** was ordered and is due about 3 days after 2026-10-10 (around 2026-10-13).

### Design notes
- 4K is not needed for general "what is this" questions (models downscale), but helps for small text, print-quality checks, and cropping a region from the full frame as a free "zoom".
- Split idea: main PC (3060 Ti) keeps speech recognition; the 1080 PC runs vision through LM Studio's OpenAI-compatible server over the home network. Main PC captures the frame, sends it, gets text back.
- The 1080 has no tensor cores, so expect a few seconds per image. Fine for on-command use, not for constant watching.
- Rook currently reaches Claude through the Claude desktop app, which is not a good path for images. Using Claude vision would likely need the API, and frames would leave the PC, so local is the better fit.
- Possible uses: checking Flashforge Adventurer 5M prints, identifying parts/labels, reading screens, help with CAD or mod setups. One camera cannot cover both the user and the printer, so mounting needs thought.
- Skip the webcam mic; keep using the headset.
- VRAM is the real constraint, not raw power. Load vision on demand, use small models, and split jobs across the two PCs. Do not buy hardware until the 3060 Ti and 1080 have been tested. A 16-24 GB GPU would only matter for a larger (14B+) local language model.

### Not decided yet
- Which vision model to use.
- Camera placement.
- Whether to add watch mode.
- The user has not said to start building.

### Suggested staged plan when the camera arrives
1. Confirm the main PC sees the webcam and a small standalone script can save one frame (OpenCV).
2. On the 1080 PC, check NVIDIA driver and LM Studio, load a vision model, and test by dragging in an image.
3. Turn on LM Studio's network server and confirm the main PC can reach it.
4. Send a saved frame from a script and time the response; compare models on small-text reading and print-quality description.
5. Hook it into Rook as a separate `vision.py` with a voice trigger.

### Before then (optional prep for the user)
Check that the 1080 PC has a recent NVIDIA driver and LM Studio installed.

### Reminders
- Back up the Rook folder before changing it, put new code in new files, work in stages, and end any update that changes Rook with a short numbered list of things to test.
- A new session needs fresh folder approval for the Rook folder, vault and this handoff folder.
- Keep private details out of notes.

---

<!-- source file: handoff-2026-10-11-drones-3d-printing-workshop-mode.md -->

## Handoff: drones, 3D printing and Rook "workshop mode" (chat started 2026-10-09 around 3:20am US Central, notes updated 2026-10-11)

Companion to `2026-10-09_Rook-session-handoff.md` (read that first for how Rook is built and how to work with the user). The only change to the PC made in this chat is stage 1 of workshop mode, described below.

### How the chat went
Started as curiosity about writing an OS for a single task, moved to a small robot built with a Raspberry Pi and the user's 3D printer, then to reprogramming a drone, then to connecting Claude, the slicer and the printer through Rook. It ended with workshop mode stage 1 being built.

### Brainstorm results (nothing bought or decided yet)
- **Task-specific OS:** easiest is a stripped Linux image (Buildroot/Yocto), then a unikernel, then fully from scratch. For a robot, Raspberry Pi OS is the right choice; a microcontroller (Arduino/Pico/ESP32) handles motors and sensors.
- **Drone paths the user likes (both):** (1) a scriptable ready-made drone, (2) a printed frame running ArduPilot or PX4 with a Pi as companion computer, later.
- **Costs given (rough estimates from memory, not verified):** a DIY 5-inch build is about $250-500 plus $50-100 for crash spares.
- **Tello:** searches showed it is an older product and listings are patchy. The user found an Amazon "Renewed" Tello at $229 (3.7 stars, 65 reviews); I advised it was steep versus the roughly $100 it historically cost. An eBay seller was also at $229. The user also showed a Fyrax drone with a 2K camera; it is a closed consumer drone with no SDK, so it does not suit reprogramming.
- **Crazyflie 2.1+ (bitcraze.io page read):** 27 g, about 7 min per battery, about 40 min charge, open-source firmware, Python client library, wireless firmware updates, expansion decks. Needs a Crazyradio (sold separately) to fly from a computer. Max payload 15 g, so it cannot carry a Pi. The page showed no price. Spare batteries are the fix for short flight time.
- **Solar:** not practical on quadcopters (a hovering quad needs far more power than the panels give). A solar fixed-wing glider (2-3 m wingspan) is the realistic version; a top-view sketch was shown. Not a plan, just an idea.

### 3D printing
- Printer: Flashforge Adventurer 5M. It sometimes drops off Wi-Fi if it runs too long, so a human stays in the loop.
- Flashforge's slicer is Flash Studio Desktop (formerly Orca-Flashforge). It supports LAN Only Mode (computer and printer on the same network), sending a file to the printer's memory list without starting the print, and USB drive printing.
- No connector exists for printers or slicers in the connector registry, so Claude cannot control them directly. Planned workflow: Claude writes CAD code (OpenSCAD or CadQuery), exports an STL, the user slices and sends it.
- An unofficial Klipper mod (Moonraker API on port 7125) exists for the 5M. It is beta, can void the warranty or damage the printer, and was not recommended unless the user wants to tinker.
- Suggested (not tried): a DHCP reservation for the printer and a firmware update to help with the Wi-Fi drops. Unverified: whether a print keeps running if Wi-Fi drops.

### Rook workshop mode (status corrected 2026-10-11)
This chat agreed the three-stage plan and built stage 1 on 2026-10-09: new `workshop_mode.py` plus three small hooks in `rook_mic.py` (import, `setup(...)`, `handle_line(...)` after the leave/shutdown check). Backup: `backups\rook_mic_backup_before_workshop.py`. `rook.py` was not touched by this chat.

Work continued after this chat. The up-to-date source of truth is the vault note `Projects/Rook-handoff.md`, section 10b, which records:
- **Stage 1:** tested 2026-10-09, all 6 tests passed.
- **Stage 2:** built and worked with real CadQuery ("make it" in workshop mode, via `workshop_cad.py` and `workshop_runner.py`; sample parts such as `simple_box_v1.stl` exist in the Rook folder's `workshop` subfolder).
- **Stage 3 (slicer and printer):** not started. It needs the Orca-Flashforge install location. Keep the human in the loop and a spoken confirmation before anything physical.

Stage 1 behavior, for reference: "Rook, workshop mode" (or "Ayah, ...") turns it on with a rising two-beep cue; lines without Rook's name are noted, not answered; "that's all" / "exit workshop mode" / 120 s of quiet turns it off.

### Things to test
Nothing outstanding from this chat. See the vault note for items the user has not tested yet.

### Open items
- Not decided: which drone to buy (Tello vs Crazyflie vs own build), and whether to try the Klipper mod.
- Unverified: whether Flash Studio's slicer can be run from the command line (matters for stage 3), and whether a print keeps running if the printer's Wi-Fi drops.
- The vault note already documents `workshop_mode.py`; no vault change was needed.

### Reminders
- A new session needs fresh folder approval for the Rook folder, the vault and this handoff folder.
- Keep private details out of notes. Keep things local where possible. New Rook functionality goes in separate files, in stages, with a numbered list of things to test at the end of each update.

---

<!-- source file: written directly in this combined file -->

## Handoff: Orbit menu sphere (chat, 2026-10-11 afternoon)

Nothing on the PC was changed except this folder. Design work only, no Rook code touched.

### What was asked
An animated digital sphere with orbiting rings that act as interactable menu options. Then: a neon gradient look, then a simulation of up to 100 options with the buttons shown as points of light until hovered, then one ring per option capped at 30 (current version).

### What exists
- `orbit-menu.html` (now in the Claude\Rook folder, moved 2026-10-12) is the full source (one self-contained file, canvas 2D, no libraries; only Google Fonts Chakra Petch and IBM Plex Mono load from the web). It also opens by double-clicking it in a browser.
- It is also published as a private Claude artifact called "Orbit Menu" (open it from the Artifacts gallery in the Claude app; the link is not repeated here).
- Look: dark ground, slowly rotating dot-sphere that fades cyan to violet to magenta, one tilted ring per option (up to 30, tilts fanned out evenly, orbit sizes and shapes varied: long radius 0.56 to 0.84 of the stage, short radius 60 to 100 percent of that, wider orbits move slower), each option a glowing light on its own ring. Hover a light to see its name in a glowing label, click it to open its detail panel. Drag turns the sphere.
- Controls: an "Options" slider (6 to 30, default 30) and an "Open" dropdown for keyboard use. A "Speak" button toggles a simulated speaking pulse: the sphere swells and glows with a fake voice level and sends out a gradient ring on each loud syllable. Real hookup is ready but unused: `window.rookSpeech.start()`, `.level(0 to 1)` while audio plays, and `.stop()` (a small local server would need to feed it from Rook's Kokoro audio). Reduced-motion setting slows everything and shows a steady glow instead of rings.
- Options: the first six are real Rook features (Conversation, Workshop, Vision, Hardware, Memory, Quest 3, text taken from the Rook notes above). The other 24 are made-up placeholders marked "Example" (Weather, Timers, Trade Bot, Printer and so on), only there to show a full menu of 30.

### Stage 1: sphere pulses to Rook's real voice (added 2026-10-11, NOT yet tested on the PC)
- New files in the Rook folder: `orb_bridge.py` (small local server, standard library + numpy only) and `rook_orb.html` (the same page as `orbit-menu.html` with a live link). Nothing new to install.
- `rook_mic.py` got 3 small additions (backup: `Rook\backups\rook_mic_backup_before_orb.py`): an optional import, `orb_bridge.start_server()` before the player thread starts, and `orb_bridge.speak(pcm, ...)` / `orb_bridge.stop()` around `winsound.PlaySound` in `play_loop`. Every bridge function swallows its own errors, so it cannot stop Rook from talking. Both files passed `py_compile`; the bridge was also tested in the cloud sandbox with fake audio (levels stream, 403 for a wrong Host header).
- How it works: before each sentence plays, the bridge measures the audio's loudness in 1/30 s steps and streams it to the page (Server-Sent Events) in time with playback. The page is served at `http://127.0.0.1:8765/` and only answers on this PC. A sentence gap shorter than 0.3 s keeps the sphere "speaking".
- Why a served page: the published artifact runs on claude.ai and cannot connect to a local server, so only the copy served by Rook shows Rook's real voice. The artifact stays a simulation.
- Settings at the top of `orb_bridge.py`: `PORT` (8765), `LATENCY` (0.04 s; raise it if the pulse runs ahead of the sound, lower if behind), `HOLD`, `HOST` (127.0.0.1; set "0.0.0.0" later so the Quest 3 can open it over Wi-Fi, but add an access code first).
- Own window (added later the same day, NOT yet tested on the PC): the user asked for a real desktop window instead of a browser tab. `rook_orb_window.py` shows the page with pywebview (no tabs or address bar). `orb_bridge.start_server()` launches it automatically (`OPEN_WINDOW = True` in `orb_bridge.py`; set False to turn off). One window only (a lock on port 8766); it reconnects by itself after "Rook, restart" and closes itself if Rook stays gone for 3 minutes. Size and always-on-top are settings at the top of `rook_orb_window.py`. Needs ONE install by the user, with the venv active in the Rook folder: `pip install pywebview` (also added to `requirements.txt`; venv is Python 3.11, which suits it). Until installed, Rook prints a hint and the browser address still works. Backups: `backups\orb_bridge_backup_before_window.py`, `backups\requirements_backup_before_window.txt`. If the window opens blank, pywebview may be using the old Windows engine because WebView2 is missing; the fix is installing Microsoft's WebView2 runtime.
- Window did not appear on the first try (16:08 run, pywebview 6.2.1 was installed in the venv, no error visible because the window runs hidden). Fix added: `rook_orb_window.py` now writes everything to `Rook\rook_orb_window_log.txt`, and if the pywebview window exits or does not start, `orb_bridge.py` falls back after 8 s to Edge or Chrome in borderless app mode (also used when pywebview is not installed). Real cause still unknown until the log is read after the next Rook start; check that file first.
- Window confirmed working by the user (16:14). Added after that, NOT yet tested on the PC: (1) a **Conversation log** under the sphere in the window: your lines addressed to Rook (by name, in the follow-up window or conversation mode, or a yes/no to a question Rook asked) and Rook's spoken replies, streamed sentences merged into one entry. System messages are left out on purpose: mode messages (`quiet_say`), the shutdown/restart goodbye, the "can only restart from the .bat" line, shutdown/stop commands, workshop-mode dictation, and all console prints. It lives in memory only (last 200 lines, cleared when Rook restarts, nothing written to disk). (2) The window **closes when Rook shuts down** (`orb_bridge.bye("quit")` runs after the goodbye finishes speaking; the window polls `/status` each second). On "Rook, restart" the window stays open and reconnects; if Rook disappears without saying goodbye (crash, console closed) it closes after 60 s. Changes: `rook_mic.py` (backup `backups\rook_mic_backup_before_chatlog.py`; `say()` got a `chat=True` option and 4 `orb_bridge.chat(...)` calls plus one `orb_bridge.bye(...)` call), `orb_bridge.py`, `rook_orb_window.py`, `rook_orb.html`. Tested in the cloud sandbox with a fake chat stream and shutdown signal.
- Startup greeting (added 16:2x, NOT yet tested): the user noticed mic-mode Rook did not greet on start (the Discord version does). `rook_mic.py` now has a `GREETING` setting near the top ("Hello, Rook here. What can I do for you?"; set to "" to turn off) and says it right after the "Rook is listening" line, through `say()`, so it also opens the follow-up window and appears in the conversation log. It plays on every start, including after "Rook, restart". Backup: `backups\rook_mic_backup_before_greeting.py`.
- Shutdown problem reported 16:20: CAUSE FOUND AND FIXED. An upload of the Orbit files at about 16:16 left OLD copies of `orb_bridge.py`, `rook_orb_window.py` and `rook_orb.html` in the Rook folder (the commit reported success but the content was the previous version), so the new `rook_mic.py` called `orb_bridge.bye()` / `.chat()` that did not exist: `AttributeError` at shutdown (aborting notes/vault sync) and on the greeting. Files re-uploaded and checked on the PC by size and by importing the module. To stop this class of problem, `rook_mic.py` now calls the bridge only through `orb(name, ...)`, which ignores a missing function or any error, so the Orbit page can never break Rook again (backups: `backups\\rook_mic_backup_before_orbsafe.py`, `...before_shutdowntrace.py`). The step-by-step shutdown trace (`rook_shutdown_trace.txt`) stays in; delete the trace code later if it is no longer wanted. Lesson: after uploading files to the PC, always compare file sizes or grep for a new function before telling the user to test.
- Inbox request 16:28 (via Rook, "check the inbox"): the user wants "different shutdown functionality". Noted in the vault (`Projects/Rook-handoff.md`, section 10D) and ticked in `Inbox.md`. Details NOT given yet: ask what they want (for example what "Rook, shut down" should do, or whether the Orbit window should behave differently) before changing anything. The vault change is saved on the PC; Rook pushes it to GitHub at its next shutdown sync.
- 16:33 two changes, NOT yet tested on the PC. (1) **Shutdown without her name during a conversation**: while conversation mode is on or the 15 s follow-up window is open, a bare "shut down", "turn yourself off", "goodbye", "bye", "good night" (optionally with okay/please/thanks/now) shuts Rook down. Added `is_nameless_shutdown()` and the `NAMELESS_SHUTDOWN = True` setting in `rook_mic.py`, plus `in_conversation()` in `conversation_mode.py` (does not use up the window). Longer sentences ("shut down the server", "turn off the lights") do not trigger it. Risk the user should know: saying "bye" to someone else within 15 s of Rook speaking will shut Rook down; set `NAMELESS_SHUTDOWN = False` to disable. Restart is not nameless. (2) **Greeting waited for the window**: the greeting now runs in a thread that calls `orb_bridge.wait_for_client(12)` first (waits up to 12 s for the Orbit window to connect, no wait if the window is off). Backups: `rook_mic_backup_before_nameless.py`, `conversation_mode_backup_before_nameless.py`, `orb_bridge_backup_before_waitclient.py` in `Rook\backups`. Edited directly on the PC and checked by compiling, importing and testing the phrase pattern, so no stale-upload risk this time.
- 16:36 **Conversation mode on by default + idle**, NOT yet tested on the PC. `conversation_mode.py`: `ON_BY_DEFAULT = True` (`rook_mic.py` calls `conversation_mode.enter(quiet=True)` at startup, no beeps or extra speech, before the greeting) and `CONVERSATION_TIMEOUT = 0` (never times out by itself; set back to 90 for the old behaviour). "Rook, idle" (also bare "idle", "go idle", "stand by", "at ease", with okay/please) turns it off and she says "Going idle. Say my name when you need me."; "Rook, wake up", "start listening" or "conversation mode" turns it back on; "that's all" still ends it too. In idle, nameless "shut down"/"goodbye" does not work (only briefly in the 15 s window after she speaks); "Rook, shut down" always works. Restarting Rook puts it back to on. Mode messages are system messages, so they stay out of the Orbit conversation log. Backups in `Rook\backups`: `conversation_mode_backup_before_default_on.py`, `rook_mic_backup_before_default_on.py`. Tested the phrases and the mode switching in a quick script. Idea not built: show "listening" / "idle" in the Orbit window.
- 16:4x Inbox requests handled. (1) **Orb scrolled off screen / conversation as its own scrolling window** (two requests, same cause): in Rook's window (`body.live`) the page is now a fixed one-screen layout; the sphere stays put, the option-detail text has a small cap, and only the conversation log scrolls (it only follows new lines if you are already at the bottom). Edited `rook_orb.html` (source copy `orbit-menu.html` in this folder); uploaded and verified by matching checksums on the PC. No restart of Python needed beyond reopening the window, but restart Rook anyway. NOT yet tested. (2) **"Interact with my desktop"**: only noted (vault `Projects/Rook-handoff.md` 10D), not started. Questions to ask the user first: what should she do first (open apps, type, click, read the screen, files)? what is allowed without asking? a stop word? Inbox ticked for the two fixes; the desktop item left open.
- 16:5x **"Add a note" works like "Remember that"** (inbox request), NOT yet tested. `rook.py`: new `ADD_NOTE_RE` and a small change to `memory_request()`; "Rook, add a note that ...", "make a note, ...", "take a note to self ..." (also without the name during conversation mode) save the fact to Memory.md exactly like "remember that" and Rook answers "Got it, I'll remember that." The phrase must start the sentence, so "do you add a note to each file?" and "can you add a note to the Claude inbox" are not taken as notes; anything with "Claude" in it still goes to the Claude inbox first. Needs 2+ words after the phrase. Tested the matching with 11 sample sentences in a script. Backup: `Rook\backups\rook_backup_before_addnote.py`. Also fixed in this round: the scrolling layout upload was stale at first (checksum mismatch caught it) and was re-sent; checksums now match. Lesson: after `device_commit_files`, wait a few seconds after copying the file to the staging folder, then verify with md5sum on the PC.
- 16:52 User reported the 16:4x-16:5x changes "seemed to work": the fixed one-screen window with a scrolling conversation, and "add a note" saving like "remember that". Still open: the "interact with my desktop" request (waiting for the user's answers to the three design questions), plus the earlier untested items (nameless shutdown, conversation mode on by default and idle, greeting after the window opens).
- 20:46 User reported via the inbox: "it all worked" (after the 20:42 test list: default-on conversation mode, greeting after the window, idle / wake up, nameless shutdown and its negative case, restart keeping one window). Treat those as confirmed. Log evidence earlier that evening: bare "Shut down." gave a clean full shutdown trace and closed the window; "Add a note that ..." saved correctly. Still open: (a) junk line `- to the clawed in-box. (added 2026-10-11)` in vault `Memory.md` from a misheard "add a note to the Claude inbox" test, plus a proposed fix ("add a note to ..." without "that" should not save to memory; teach Rook that "clawed in-box" means the Claude inbox) waiting for the user's yes; (b) the desktop-interaction request, waiting for answers to the three design questions.
- 20:5x **Faster way for Rook to message Claude** (user: the extra step felt long), NOT yet tested. `rook.py`: `SEND_CONFIRM = False` (no yes/no) and new `SEND_FULL_TEXT = True`: "Rook, tell/ask/message/notify Claude ..." saves the request to the vault inbox as a backup AND immediately types the actual words into the Claude app as `Rook here: <request> (also in the vault inbox)` (over 300 characters it is cut with a pointer to Inbox.md), then Rook says "Sent." (or "I couldn't reach the Claude app, but it's saved in your inbox."). "Rook, note for Claude ..." / "request for Claude ..." only saves to the inbox and says "Noted for Claude. It's in your inbox." (`NOTE_ONLY_RE`). Setting `SEND_CONFIRM = True` brings the yes/no back; `SEND_FULL_TEXT = False` goes back to the fixed "please check the inbox" line. When such a message arrives, tick the matching inbox item (the text says it is also in the inbox). Backup: `Rook\backups\rook_backup_before_directsend.py`. Tested the phrase matching and the typed text in a script. Limits unchanged: the Claude app must be open; the text lands in whichever chat is open; Claude's reply is not spoken back.
- 20:52 Direct sending CONFIRMED working: "Rook, tell Claude we should test the new sending" arrived in the Claude app with the full words (`Rook here: ... (also in the vault inbox)`), took about 2.5 s end to end, and the inbox copy was saved. Not yet tried: "note for Claude" (inbox only) and the Claude-app-closed fallback.
- 20:52 **Second window after "Rook, restart"**: cause found and fixed, NOT yet tested. The pywebview window logic itself worked (`rook_orb_window_log.txt` shows "a window is already open; this copy exits" at 20:46 and 20:52). The extra window was the Edge/Chrome app-mode FALLBACK in `orb_bridge.py`: it decided "no window is open" by connecting to the window's lock port, which only accepts a couple of connections before refusing, so after a restart or two it wrongly concluded no window existed and opened Edge. Fix: `rook_orb_window.py` now exits with code 10 when a window is already open (0 = closed normally, 1 = crash, 11 = pywebview missing) and the bridge opens the fallback only for other non-zero codes. Edited directly on the PC, compiled; backups `orb_bridge_backup_before_exitcodes.py`, `rook_orb_window_backup_before_exitcodes.py`. The extra Edge window from today has to be closed by hand; the already-open window from the old run keeps the old code until closed. Test: restart Rook twice and confirm only one window.
- Not covered yet: Discord voice (`rook_discord.py` plays through a different path), and the page only displays; clicking an option does not run Rook commands yet.

### Session end 2026-10-11 (about 4:53 pm US Central; user stopped for a nap, usage limit near)
- Orbit work started about 3:37 pm. State: everything above is saved on the PC (Rook folder, Claude Handoff folder, vault). Backups of every changed Rook file are in `Rook\backups`.
- Confirmed working by the user: the Orbit window, the conversation log, the fixed scrolling layout, "add a note", and (earlier) the window opening and the sphere pulsing with Rook's voice.
- Built but not yet reported on: nameless "shut down"/"goodbye" during a conversation, conversation mode on by default with "Rook, idle" / "Rook, wake up", greeting that waits for the window, the shutdown trace file (`rook_shutdown_trace.txt`).
- Open: the "interact with my desktop" request (ask the three design questions first), vault changes not yet pushed to GitHub (Rook pushes at its next shutdown), Discord voice does not drive the sphere.
- Start of next session: read this section, ask how the untested items went, then the desktop questions.

### Orbit menu: console window setting (2026-10-11)
- Rook's cmd console is now hidden when Rook starts (orb_bridge.py: CONSOLE_AT_START=False, hide_console_at_start(), set_console(); rook_mic.py calls it right after the startup banner).
- The Orbit window has a "Settings" dropdown with a "Show console window" checkbox (page POSTs /console on 127.0.0.1 only; page checks origin).
- Safety: the console is shown again at exit (so errors and "Rook has stopped" can be read), and if no Orbit window connects within 45 s.
- Relies on the classic console host (fine on Windows 10; Windows Terminal would not hide).
- Backups: Rook\backups\rook_mic_backup_before_console.py, orb_bridge_backup_before_*.py. Page copies: Rook\rook_orb.html, Claude\Rook\orbit-menu.html (was Claude Handoff\orbit-menu.html until 2026-10-12; md5 b6166054...). Artifact version 11.
- Tested on the PC (2026-10-11): hidden at start, Settings checkbox show/hide, menu close, console back at shutdown, single window on restart all worked. Not tested (user said fine): console returning after 45 s when no window connects.

### Not done / open
- Clicking an option only shows its description; it does not run anything.
- Not checked in a browser by Claude (no preview was available). The user said it looked good, but speed at 30 rings on their PC is untested.
- Ideas if the user wants them: smaller lights or thinner rings if 30 feels crowded; make it Rook's status display (glow when listening or speaking); show it on the Quest 3 front end; wire clicks to real Rook commands through a small local server.

### Things to test
1. Open `orbit-menu.html` from the Claude\Rook folder in a browser and confirm the sphere animates smoothly with the slider at 30.
2. Hover a few lights and confirm the name label appears and the cursor becomes a pointer.
3. Click a light and confirm the detail panel and the "Open" dropdown both update.
4. Press Speak and confirm the sphere swells and rings spread out in time with the pulses; press Stop and confirm it settles.
5. Stage 1 (needs Rook running): start Rook with `Start_Rook_Mic.bat`, confirm the console prints `[orb] Orbit page: http://127.0.0.1:8765/`, open that address in a browser, and confirm the corner text says "Rook: connected".
6. Own window: run `pip install pywebview` in the Rook folder with the venv active, restart Rook, and confirm a plain window (no tabs) opens by itself, then check it shows "Rook: connected".
7. Say "Rook, restart" and confirm only one window is open afterwards and it reconnects.
8. Ask Rook a question: confirm the sphere pulses with its actual voice, and calms down after it finishes.
9a. Start Rook: confirm the window is open BEFORE she says the greeting.
9b. After any answer (within 15 s), say just "shut down" or "goodbye" and confirm Rook shuts down; also say "shut down the server" and confirm she does NOT.
9. Conversation log: say "Rook, what time is it?" and confirm "You" and "Rook" lines appear in the window; say "Rook, conversation mode" and confirm that system message does NOT appear.
10. Say "Rook, shut down" and confirm the window closes after the goodbye; start Rook again and confirm a fresh, empty log.
11. Say "Rook, restart" and confirm the window stays open and reconnects.
12. Interrupt Rook mid-sentence (talk over it or say stop): confirm the pulse stops with the sound.
13. Drag the sphere to turn it, and drag the slider down to 6 to see the small version (the 100-option dot version was replaced).

---

## Handoff: Rook weather lookup for other towns (cloud session, 2026-10-11 about 4:15 to 4:55 pm US Central)

### What was asked
Rook (by voice) left a request to "check the inbox". The inbox item turned out to be a test; the real request was in Rook's `Memory.md` (added 2026-10-11): give Rook the ability to look up the weather for different locations instead of one set location. The user asked for a handoff note at the end.

### What was found
- Rook could already look up other towns (`queries.py` geocodes with Open-Meteo), but only when the sentence contained "weather" plus in/for/at/near (for example "weather in West Plains").
- At 16:11 the user asked "Can you check the weather?" (Thayer answered: 88 degrees and clear), then "What about West Plains?". That line has no "weather" in it, so it skipped the lookup and went to the chat model, which guessed. Rook then wrongly said it could not look up other towns.
- The inbox ("For Claude") only holds five items: four old test lines from 2026-10-09 and "check the inbox". Nothing else was waiting there. The user has not yet said whether to clear the four old test lines.

### What changed (NOT yet tested on the PC)
- `rook.py`: new `weather_followup()` and `WEATHER_FOLLOWUP_RE`. For 180 seconds after a successful weather answer, "what about X?", "how about X?", "and X?" or "and in X?" runs the weather lookup for X. Guards: place must be 5 words or fewer and must not start with my/your/the/then/that/this/it/you/me. New `state["last_weather"]` timestamp is set after each successful weather reply.
- `queries.py`: `find_place()` now fetches up to 20 matches even with no state given and prefers one in the home state (taken from `DEFAULT_CITY`, "Thayer, MO", so Missouri) so "West Plains" should resolve to Missouri. If a state is spoken ("Springfield, Illinois") it is still respected.
- Both files compiled cleanly (`py_compile`) in the cloud sandbox; the regex was checked against sample sentences. The network lookup itself was not run here.
- Backups: `Rook\backups\rook.py.before-weather-followup` and `Rook\backups\queries.py.before-weather-followup`.

### Things to test
1. Restart Rook. Say "Rook, what's the weather?" and confirm Thayer still works.
2. Right after, say "What about West Plains?" and confirm a real reading for West Plains, Missouri.
3. Say "How about Chicago?" and confirm Chicago, Illinois (not a Missouri match).
4. Say "What's the weather in Springfield, Illinois?" and confirm the state is respected.
5. Wait more than 3 minutes, then say "What about West Plains?" and confirm it goes to normal chat, not a lookup.
6. Check `rook_debug_log.txt` for "weather lookup: <town>" lines and any "[weather error]".

### Open items
- Rook told the user it "can't send anything to Claude"; at 16:13 it did send "check the inbox" to the Claude app. The wording of that earlier reply may be worth checking.
- Rook's `Memory.md` still contains the original note about location lookup; the user can delete it once the feature is confirmed working.
- Optional: clear the four old test lines from the vault `Inbox.md` (ask the user first).

### Reminders
- This session needed fresh folder approval for the Rook folder, the vault (`Documents\GitHub\Rook-vault`), and `Claude Handoff`; a new session will need it again (`device_request_folder_access`).
- Two folders named `Rook-vault` also exist (`Desktop\Rook-vault` and `~\Rook-vault`); both are empty apart from `.obsidian`. The real vault is `Documents\GitHub\Rook-vault`.
- User preference: end Rook updates with a numbered "things to test" list; back up before edits.

---

## Handoff: Rook desktop skills (skills.py) and shutdown/restart fixes (2026-10-11 evening)

Moved here from the Skills-folder notes, where these Rook updates had been appended by mistake. Companion to section 1 (read that first). Backups of every changed file are in `Rook\backups`.

### Rook desktop skills, stage 1 (2026-10-11, built, NOT yet tested)
- New file Rook\skills.py (the "Skills" file). rook.py asks skills.matches(text), runs skills.handle(text); rook_mic.py turns it on (skills.enable(True)). Discord voice can never use it.
- FREE (done at once): open approved apps/folders/websites (lists at top of skills.py), "google X", list windows, switch to a window, show desktop, scroll, volume up/down/set/mute, play-pause/next/previous, screenshot (saved in Rook\screenshots).
- ASK first (spoken yes): "type ...", "press <keys>" (Alt+F4, Ctrl+Alt+Del blocked), "close <window>" (never Rook), "lock the computer".
- "Rook, stop everything" cancels anything waiting; mouse into a screen corner stops pyautogui; "turn off/on desktop control" is a master switch; every action is logged in Rook\rook_skills_log.txt.
- Defaults chosen because the design questions were not answered; user can change the lists or which skills are free vs ask.
- Not built: clicking by name, reading the screen, forms (stage 2, after stage 1 is tested).
- Backups: Rook\backups\rook_backup_before_skills.py, rook_mic_backup_before_skills.py.
- Update (21:5x): ending a desktop request with the word "confirm" skips the yes/no question ("Rook, close notepad, confirm"). Blocked keys (Alt+F4 etc.) stay blocked. Backup: Rook\backups\skills_backup_before_confirm.py. Untested.
- Update (21:5x): after "close <window>", Rook watches ~2.5 s for a save-changes dialog (Windows UI Automation; reads only the question text, never the document), reads it out ("It asks: ... Say save, don't save, or cancel."), then clicks the Save / Don't Save / Cancel button you name. Unclear speech is ignored (normal handling); "stop everything" leaves the dialog alone. Untested on real apps (Notepad and Word dialogs are the ones to try). Backups: Rook\backups\skills_backup_before_savedialog.py, rook_backup_before_savedialog.py.
- Update (22:0x): log check showed open/close/type/confirm/save-dialog all worked (the 02:49 save-dialog lines in rook_skills_log.txt are my own simulated test, ignore). Typing went into whatever window was active, so now "type X in <window>" and "press <key> in <window>" bring that window to the front first (only if it is an approved app or an open window; otherwise nothing is typed). "type ... in the park" style text is still typed as is. Discord: she can open and focus it and type/press Enter once it is focused, but cannot click channels or the message box yet (needs stage 2: clicking by name). Backup: Rook\backups\skills_backup_before_focus.py. Untested.
- Update (22:1x), from the skills log: "type hello in notepad" with Notepad closed said "I don't see a window" (correct but unhelpful); "...in Notepad again" typed the whole phrase because of the trailing "again". Fixed: trailing again/please/now/too/for me are ignored, and an approved app that is not open yet is opened (up to ~8 s) and focused before typing. "type test in discord" reported success; whether the text landed in the message box was not reported. Backup: Rook\backups\skills_backup_before_openfocus.py. Untested.
- Confirmed by user (22:02): open-then-focus before typing, trailing "again/please" handling, and "type test in discord" all worked.
- Stage 2 start (22:1x): Discord messaging by name. "Rook, send a message to Leon" opens Discord, uses its Quick Switcher (Ctrl+K, @Leon, Enter - no mouse clicking needed), checks Discord's window title contains the name (aborts and sends nothing if not), asks "What should I say?", reads the message back, sends on a yes (or "confirm" at the end of the message). "...to Leon saying hi" does it in one go with a yes first. Nicknames: DISCORD_PEOPLE in skills.py. Not yet built: clicking arbitrary things by name, reading the screen. Backup: Rook\backups\skills_backup_before_discord.py. Untested on real Discord.

### Restart/shutdown hang fix (2026-10-11 22:1x)
- Finding: "Rook, restart" (and sometimes shut down) hung. rook_shutdown_trace.txt stopped after "vault synced" in 3 of 4 recent shutdowns (21:49, 21:53, 22:05); realtimesst.log ended at "Finishing preview transcription thread". So RealtimeSTT's recorder.shutdown() sometimes never returns, Python never exits, and Start_Rook_Mic.bat never sees exit code 4. Notes and vault sync were fine. (The Orbit window closed itself ~60 s later: "Rook is gone".)
- Fix (rook_mic.py): shutdown_recorder() gives the recorder 8 s (RECORDER_SHUTDOWN_SECONDS), then kills its helper processes (not the Orbit window), the remaining shutdown steps run, and if it had hung Rook leaves with os._exit after running the normal exit clean-up (console re-show, lock release). Exit code 4 still restarts. Backup: Rook\backups\rook_mic_backup_before_hangfix.py. Untested.
- To check afterwards: rook_shutdown_trace.txt should end with "report written" (and "recorder shutdown hung: killing its helper processes" / "leaving now" if it hung).

---

## Handoff: Discord API for Rook, paused (chat, 2026-10-11 about 10:00 to 10:10 pm US Central)

Companion to `2026-10-09_Rook-session-handoff.md` (section 1 above; read that first for how Rook is built and how to work with the user). Nothing on the PC was changed in this chat. It was a question and a short design discussion, and the user then paused the feature.

### The question
Does the Discord API have functions Rook can connect to, instead of going through the Discord UI?

### Answer given
Yes. Discord has an official bot API:
- REST API: send, edit and delete messages, reactions, read channel history, channels, roles, members, threads.
- Gateway (WebSocket): live events such as new messages and reactions (how Rook would "listen").
- Slash commands / interactions, and webhooks (post-only, no bot or token needed, just a URL).
- Voice: bots can join voice channels and play audio. Receiving and transcribing other people's audio is more limited. Discord has been tightening voice encryption, so a library's voice support would need checking.
- Setup path: Developer Portal application, Bot token, intents (reading message text needs the privileged Message Content intent), OAuth2 invite link, then `discord.py` (Python), which fits Rook.

### How this relates to what Rook does today
Rook's Discord messaging (`skills.py`, stage 2 start) drives the UI: opens Discord, Quick Switcher (Ctrl+K, @name, Enter), checks the window title contains the name, asks "What should I say?", reads it back, sends on a yes. Discord voice is a separate path (`rook_discord.py`). The API would replace the keystroke steps, not the spoken confirm flow.

What the API does better: no dependence on Discord being open or focused or on window titles; sends to a channel by ID; Rook could read a channel aloud, which UI automation cannot do without screen-reading.

### The catch (main point to remember)
- A bot or webhook posts as the bot ("Rook"), not as the user. A bot can DM a person only if they share a server with it and allow DMs from server members.
- Sending as the user would need their personal account token. That is self-botting, it breaks Discord's Terms of Service and can get the account banned. Not recommended and not to be built.
- So the API suits posting to a private channel in the user's own server (alerts, reminders, TradeBot reports, a Rook channel). Messages that must appear to come from the user stay on the existing UI method.

### Decision
The user said: pause this feature for now. Nothing was decided or built.

### Not decided yet
Whether Rook should post as a bot in a server channel, or whether messages must appear as coming from the user. This was asked and not answered.

### Suggested first step if resumed
1. Back up the Rook folder first; put new code in a new file (e.g. `rook_discord_api.py`) that `skills.py` calls; keep the Ctrl+K UI method as the fallback.
2. Start with a webhook for "post to a channel" (no token, no bot).
3. Add a small bot only if reading messages or DMs are wanted. Keep the bot token in a `.env` file, never in chat or in handoff notes.
4. Keep the spoken read-back and yes before anything is sent. End any update that changes Rook with a short numbered list of things to test.

### Reminders
- A new session needs fresh folder approval (device_request_folder_access) for the Rook folder, the vault and this handoff folder. This chat was granted this handoff folder only.
- Another session was appending to this file while this chat ran, so re-check the file's size and modified time right before editing it.
- Keep private details out of notes. Keep things local where possible.

---

## Handoff: Rook-Vision, EMEET Pixy + local vision AI (chat, 2026-10-13 about 9:25 pm US Central)

Continues "Rook webcam / vision brainstorm" above (the 4K webcam turned out to be an EMEET Pixy). Read that section for the reasoning (local only, test the GTX 1080 PC, no training needed).

### Asked
Create a project that uses the EMEET Pixy and a local image recognition AI so Rook can see the user.

### Done
- New folder `Rook-Vision\` in this Claude folder (see its `README.md`, written as a step-by-step guide). Nothing in the Rook program or on the Desktop was changed; no backup needed yet.
- Scripts: `setup.bat` (venv + OpenCV), `list_cameras.py`, `capture_frame.py` (one photo or live preview, 1080p or 4K), `vision_client.py` (talks to LM Studio's OpenAI-style local server), `ask.py` (photo + question, or `--image`, `--models`, `--server`), `benchmark.py` (same photo, several models, timed, report in `results\`), `presence.py` (OpenCV face check, no AI model), `vision.py` (what Rook will import later: `handle(spoken_text)` returns a reply or None; spoken triggers in `TRIGGERS`), `config.json`.
- Tested here only: scripts compile; the client, `ask.py`, `benchmark.py` and `vision.handle` work against a fake local server with a fake image; the "server not reachable" message works.
- Facts checked on the web (reviews, not tested by us): Pixy is 4K/30 or 1080p/60, USB-C, standard UVC webcam. Gimbal/AI tracking appear to be EMEET Studio features, so scripts do not steer the gimbal. A Windows Central review reported the Pixy's LED is not wired to the sensor, so the code opens the camera for about a second per question and releases it. Model guide (insiderllm.com) lists Qwen3-VL 8B, Qwen2.5-VL 7B and Gemma 3 12B as fitting 8 GB at Q4.

### Untested / open
- Nothing has run against the real Pixy or a real LM Studio vision model.
- Not decided: which model; which PC runs it (3060 Ti main PC vs GTX 1080 PC); camera placement; always-on watch mode; face recognition (deliberately not included).
- Stage 4 (hooking `vision.py` into Rook) not started. Needs folder approval for the Rook folder on the Desktop, a backup first, and a look at how Rook handles voice commands.
- A `__pycache__` folder was left in `Rook-Vision\` by a test run; it is harmless and can be deleted.

### Things to test
1. Run `setup.bat` in `Rook-Vision\`, then `python list_cameras.py`; confirm the Pixy shows and set `camera_index` in `config.json`.
2. `python capture_frame.py --preview`, then `python capture_frame.py`: sharp photo saved in `snapshots\`? Try `--width 3840 --height 2160` too. Does EMEET Studio need to be closed?
3. In LM Studio load a vision model (eye icon), start the server, then `python ask.py "Can you see me? What am I doing?"`.
4. Repeat with the model on the GTX 1080 PC (Serve on Local Network, then `--server http://<ip>:1234/v1`). Note how many seconds it takes.
5. Hold something with small printed text, take a photo, and run `python benchmark.py <photo> --models ...`; compare how well each model reads it.
6. `python presence.py`: does it say "face seen" when you sit down and "nobody in view" when you leave?

### Update, same chat (about 9:30 to 9:50 pm US Central): camera works, hooked into Rook
- User ran the stages: `list_cameras.py` showed Logi C270 (0), EMEET PIXY (1), EMEET STUDIO Virtual Camera (2). Index 1 would not open while EMEET Studio was running (it holds the camera); after closing Studio it worked. `camera_index` is now 1 in `Rook-Vision\config.json`. `ask.py` with a vision model loaded in LM Studio (Qwen3-VL 8B suggested) answered and "saw me". Seconds per answer not reported yet. Run the scripts with `venv\Scripts\python ...` (plain `python` lacks OpenCV).
- Stage 4 done (NOT yet tested with Rook running). Backups first: `Rook\backups\rook_backup_before_vision.py`, `Rook\backups\rook_mic_backup_before_vision.py`.
  - New `Rook\rook_eyes.py`: `matches(text)` / `answer(text)` like `rook_hardware.py`. It runs `Rook-Vision\look.py` with Rook-Vision's own venv Python as a subprocess, so Rook's venv needs nothing new (no OpenCV in Rook's venv). Settings at the top (ENABLED, TIMEOUT_SECONDS, paths). Log: `Rook\rook_eyes_log.txt`.
  - New `Rook-Vision\look.py`: prints only the spoken answer (exit 1 plus a message on problems).
  - `rook.py`: added `VISION_ON` plus the `rook_eyes` import (after the hardware import), and an `elif` branch just before the hardware branch. Rook says "Let me take a look." then the answer.
  - `rook_mic.py`: one line after `skills.enable(True)` calls `rook_eyes.enable(True)`. Discord voice never turns it on, so a friend in a call cannot make Rook use the camera (`matches()` returns False unless enabled).
  - Voice: "can you see me", "am I there", "what am I holding/wearing/doing", "look at this", "what's in my hand", "read this/the label", "what do you see", "take a look", "what's on my desk", bare "what is this". "turn off the camera" / "turn on the camera" switches it. Requests over 18 words are ignored so normal questions still go to the AI. Edit `TRIGGERS` in `rook_eyes.py` to change phrases.
  - Tested here: compile, phrase matching (no overlap with `skills.matches` or `rook_hardware.matches` on the test phrases), the subprocess path with a fake script, the error messages, and the Discord-blocked behavior. Not tested: real Rook run.
- Needs running: LM Studio server on with a vision model, EMEET Studio closed (or it holds the camera).
- Noticed, not changed: `skills.py` FOLDERS still points "handoff" to `Desktop\Claude Handoff` (folder is now `Desktop\Claude`).

### Things to test (Rook with vision)
1. Close EMEET Studio, start LM Studio's server with the vision model, then start Rook (`Start_Rook_Mic.bat`). Look for a "[vision] not available" line at startup; there should be none.
2. Say "Rook, can you see me?" Expect "Let me take a look." then a description. Note how many seconds it takes.
3. Hold up an object: "Rook, what am I holding?" and "Rook, read this label".
4. Say "Rook, what's the weather?" and "Rook, how much RAM do I have?" to confirm those still work.
5. Ask a normal question with the word "this", e.g. "Rook, what is this error mean"; it should go to the AI, not the camera.
6. Quit LM Studio's server and ask again; Rook should say it can't reach the vision model. Then close and reopen EMEET Studio and ask; Rook should say it can't open the camera.
7. "Rook, turn off the camera", then "can you see me" (should not look), then "turn on the camera".
8. Check `Rook\rook_eyes_log.txt` shows each request.

### Result (same chat, about 9:41 pm US Central)
User tried Rook with the camera and reported everything seems to work well. No problems reported. Exact seconds per answer and the full "Things to test" list above were not itemized, so treat items 4 to 8 (other features still fine, normal questions not hijacked, error replies, camera off/on) as unconfirmed unless the user says otherwise.
Ideas not started: compare models with `benchmark.py`, try the 1080 PC for vision, `presence.py` as a cheap "is anyone there" gate, a watch mode, camera placement for the printer.

### Speed follow-up and plan for tomorrow (same chat, about 9:45 pm US Central)
- Rook-Vision works but answers slowly on the main PC. Likely cause: the 3060 Ti's 8 GB is shared by Rook's speech recognition and voice plus the vision model. User set LM Studio's model unload time to "never unload" (stops reloads between questions); effect not yet measured.
- Added timing: `Rook-Vision\look.py` now prints "timing: camera Xs, model Ys" to stderr and `Rook\rook_eyes.py` writes it into `Rook\rook_eyes_log.txt` (restart Rook to use). Backup: `Rook\backups\look_backup_before_timing.py`.
- Tomorrow (user's plan): move some work to the GTX 1080 PC. Start with running the vision model there: LM Studio on the 1080 PC with "Serve on Local Network", then set `server_url` in `Rook-Vision\config.json` to `http://<1080 PC IP>:1234/v1` (test first with `ask.py --server ...`). Other speed ideas if needed: Instruct (not Thinking) model, `max_image_side` 768, a 4B vision model, full GPU offload.

### Things to test
1. Restart Rook, ask "can you see me" twice, and read the `timing:` line in `Rook\rook_eyes_log.txt`. Is the second answer faster than the first (model staying loaded)?
2. Tomorrow: after pointing `server_url` at the 1080 PC, compare timing with the model on the main PC.

### End of session note (about 9:46 pm US Central)
- Rook health report for 9:37 to 9:44 pm (mic mode, with the vision model loaded): GPU memory averaged about 6.9 GB and peaked about 7.9 GB of the 3060 Ti's 8 GB, so the card is nearly full. This fits the theory that the vision model competes with Rook's speech models for VRAM. Everything else healthy (speech to text 0.56 s avg, Claude replies 2.5 s avg, no errors). The report does not time camera requests; use the `timing:` line in `Rook\rook_eyes_log.txt`.
- Paused for the night. Pick up tomorrow with: (1) move the vision model to the GTX 1080 PC (see the plan in the previous section), (2) compare the `timing:` numbers before and after, (3) optionally `benchmark.py` to choose the model.
- Start a new chat for it (START-HERE rule 7). It needs fresh folder approval for `Desktop\Claude` and `Desktop\Rook`.


## Handoff: Rook-Vision on the 2nd PC, Stage 5 remote camera (chat, 2026-10-27 about 12:10 pm US Central)

Continues "Rook-Vision, EMEET Pixy + local vision AI" above ("plan for tomorrow": move vision to the GTX 1080 PC).

### Asked
"Set up LM Studio and Rook with video connection on my 2nd PC." Clarified in chat: the linked computer is the main PC; the Pixy camera MOVES to the 2nd PC (not just the model).

### Done
- Design: 2nd PC runs LM Studio plus a tiny HTTP service; Rook on the main PC asks it and gets text back. No images cross the network. `rook_eyes.py` and Rook were NOT changed.
- Backups first: `Rook-Vision\backups\look_backup_before_remote.py`, `config_backup_before_remote.json`.
- New: `vision_server.py` (POST /look {question}, GET /health, one request at a time, optional token), `common_light.py` (config loader without OpenCV), `Start_Vision_Server.bat`, `Open_Firewall.bat` (port 8765, private networks, run once as admin).
- Changed: `look.py` now has two modes; if `remote_url` in `config.json` is set it calls the 2nd PC, otherwise the original local camera path. `config.json` gained `remote_url` (empty), `server_port` (8765), `server_token` (empty). README has a new Stage 5 with the steps.
- Tested here only: compile; server + look.py against a fake LM Studio and fake frame (answer, health, bad token = 401, server-down message); local mode unchanged.

### Untested / open
- Nothing run on the real 2nd PC: LM Studio install, GTX 1080 speed, Pixy on that PC, firewall rule, `Start_Vision_Server.bat`, Rook end to end.
- The 2nd PC's IP is unknown; a fixed IP or router reservation is advisable. Haven't checked whether Python 3.11 is on the 2nd PC (`setup.bat` needs `py -3.11` or `python`).
- Server window must stay open on the 2nd PC (no auto-start yet). Main PC's camera index 1 setting is irrelevant in remote mode.
- Still open from before: `skills.py` FOLDERS points "handoff" to the old `Claude Handoff` path.

### Things to test
1. 2nd PC: copy folder, run `setup.bat`, `venv\Scripts\python list_cameras.py`, set `camera_index`.
2. 2nd PC: LM Studio vision model loaded, server on, `venv\Scripts\python ask.py "what do you see"` works locally there; note seconds.
3. 2nd PC: `Open_Firewall.bat` as admin, then `Start_Vision_Server.bat`.
4. Main PC browser: `http://<2nd PC IP>:8765/health` shows ok and the model.
5. Main PC: set `remote_url`, then `venv\Scripts\python look.py "can you see me"` from `Rook-Vision`.
6. Start Rook: "Rook, can you see me?" and "what am I holding?"; read the `timing:` line in `Rook\rook_eyes_log.txt` and compare with the old main-PC numbers.
7. Turn off the 2nd PC's server and ask again; Rook should say it can't reach the vision PC.


### Result, same chat (2026-10-27 about 2:10 pm US Central): remote camera works
- 2nd PC set up by the user: Python 3.11 installed with winget (`Python.Python.3.11`) after "python was not found"; `setup.bat` then worked. Camera index: the "EMEET STUDIO Virtual Camera" gave a black frame, so `camera_index` is the real EMEET PIXY (EMEET Studio must stay closed on that PC). LM Studio models on that PC: `qwen/qwen3-vl-8b`, `qwen/qwen3.8-27b`, nomic embed. Firewall rule and `Start_Vision_Server.bat` done. Browser needed `http://` (https gives ERR_SSL_PROTOCOL_ERROR); `/health` returned ok.
- Main PC `Rook-Vision\config.json`: `remote_url` = `http://192.168.58.106:8765` (2nd PC IP; may change without a router reservation).
- `look.py "can you see me"` from the main PC answered correctly: `timing: remote camera 2.6s, model 21.4s`. Probably includes a cold model load; warm timing not yet measured.
- Suggested, not confirmed done: set `"model": "qwen/qwen3-vl-8b"` in the 2nd PC's `config.json` so LM Studio does not pick the 27B model.
- Not yet tested: through Rook by voice, and the other Stage 5 items in the list above.
- Later, same chat (about 2:20 pm): the server failed with "No module named cv2" when started from the .bat even though OpenCV was installed in the venv (the bat's `activate` step fell back to another Python on the 2nd PC). Fix: bat now calls `venv\Scripts\python.exe vision_server.py` directly (the user made this edit on the 2nd PC; the copy in `Rook-Vision\` here is updated to match). User confirmed everything is working. Still unrecorded: warm timing after full GPU offload, and the Rook voice test.
- Rook voice test (about 2:22 to 2:35 pm): first request at 14:22 timed out at 150 s (Rook was blocked inside the look call, so a second phrase waited too); cause not confirmed (model was not pinned; the user later confirmed only qwen3-vl-8b loaded and `model` set in the 2nd PC's config). Retry at 14:34 worked through Rook: `timing: remote camera 2.9s, model 23.2s`. So the remote path works by voice, but the model step is still about 23 s on the GTX 1080.
- Open: speed (try the 4B model, `max_image_side` 768, check GPU offload is full); a timeout still blocks Rook for up to 150 s (could lower `TIMEOUT_SECONDS` in `rook_eyes.py`); 2nd PC IP reservation; server window must be started by hand after reboot. Items 3 and 4 of the earlier test list (server-off message, other commands still fine) not confirmed.

## 2026-10-27 (main PC) - resolved: old handoff history merged
The open item above (main PC history not in the repo) is done: the old Rook, TradeBot, Skills and Misc notes are appended in their own files, plus new Productivity.md and 2026-10-24_RimWorld-test-mod.md. Details and a test list are in the last section of Handoffs/Misc.md.

## 2026-10-27 (main PC session, afternoon) - Rook sees again after the repo move; slow first look
Asked: Rook on the main PC could not see the vision server on DESKTOP-2 after Desktop\Claude became the git clone; first "can you see me" was very slow in LM Studio; add timing logs; auto-load the model.
Done:
- Cause of "can't see": `Rook\rook_eyes.py` hardcoded `Desktop\Claude\Rook-Vision`, which moved to `Desktop\claude-old\Rook-Vision`. Changed VISION_DIR to point there (backup `Rook\backups\rook_eyes_backup_before_claude-old_path.py`). Confirmed working by the user.
- Added timing to Rook's log (`Rook\rook_eyes_log.txt`): a "rook_eyes loaded (Rook started)" line, `look #N since Rook started`, full camera/model timing (was cut at 80 chars), and `total X.Xs` on replies, failures and timeouts. Backup `Rook\backups\rook_eyes_backup_before_timing_log.py`. Not yet run (needs a Rook restart).
- DESKTOP-2 `config.json` had a typo in `model` (digit 1 instead of letter l in "qwen3-vl-8b"); the user fixed it on DESKTOP-2.
- `Start_Vision_Server.bat` now runs `lms server start` and `lms load qwen/qwen3-vl-8b --gpu max --context-length 8192 -y` before starting `vision_server.py` (falls back to `%USERPROFILE%\.lmstudio\bin\lms.exe`). Flags not verified on the user's LM Studio version.
- DESKTOP-2 is now a git clone (done in place: git init, fetch, reset --hard origin/main). Old loose `Rook-Vision\` folder there is still to be retired after the new copy is confirmed.
Open:
- Main PC still uses `claude-old\Rook-Vision` (has the venv and `remote_url`); the repo's `config.json` has `remote_url` empty, so moving it into the repo needs a per-PC settings file (gitignored).
- Cold-load time of the model on the GTX 1080 not yet measured with the new log; smaller image (`max_image_side` 768) or a 4B model are the next levers.
Things to test:
1. DESKTOP-2: `git pull`, then in a NEW Command Prompt run `lms --version`; if not found, run `%USERPROFILE%\.lmstudio\bin\lms.exe bootstrap`.
2. DESKTOP-2: eject the model in LM Studio, double-click `Start_Vision_Server.bat`; the window should show the server starting and the model loading, then the vision server. LM Studio should show qwen3-vl-8b READY, GPU offload full, context 8192.
3. Main PC: restart Rook; `rook_eyes_log.txt` gets "rook_eyes loaded (Rook started)".
4. Ask "Rook, can you see me?" twice; send the two `total X.Xs` values (look #1 vs #2).
5. If `lms load` errors, run `lms load --help` on DESKTOP-2 and send the output.

## 2026-10-27 (main PC session, late afternoon) - shorter Rook-Vision answers
Asked: speed up "can you see me" by capping answer length (option 1 of the speed options).
Why: LM Studio log on DESKTOP-2 showed generation at about 10.7 tokens/s (about 94 ms per token, 46 tokens = 4.2 s of a 6.4 s request); an earlier 31-token answer was faster. Image shrink (max_image_side 768, 1280x720, warmup_frames 5) cut prompt tokens 681 -> 441 and the camera step about 0.4 s, but did not help the model step.
Done:
- `vision_client.py` (repo, DESKTOP-2 server): system prompt now asks for one short sentence (about 20 words) unless asked to read text; `ask_image` max_tokens is now `max_answer_tokens` from config.json, default 80 (was 300). The key is not in config.json yet, so the default applies.
- `Rook\rook_eyes.py` (main PC): the three description questions now ask for one short sentence (the "read the text" question is unchanged). Backup `Rook\backups\rook_eyes_backup_before_short_answers.py`.
Not done / open:
- Not run yet: needs `git pull` on DESKTOP-2 and a restart of the vision server (it imports vision_client at start) plus a Rook restart.
- `claude-old\Rook-Vision\vision_client.py` on the main PC (used only in local-camera mode) still has the old prompt.
- Other speed ideas: try the 4B model; Flash Attention off on the 1080; close other GPU users (7.6 of 8 GB VRAM in use); keep the camera open in the server (code change).
Things to test:
1. DESKTOP-2: close the vision server window, `git pull`, start `Start_Vision_Server.bat` again.
2. Main PC: restart Rook, ask "Rook, can you see me?" three times; send the `total` lines. Expect a one-sentence answer and a model time of about 4 s (was 7 to 10 s).
3. Ask "what's on my desk" and "what am I holding" once each and check the answers are still complete sentences, not cut off.
4. Ask Rook to read a label or screen text; it should still read it fully (cap is 80 tokens).


## 2026-10-27 (main PC session, evening) - Rook starts the vision server on demand

**Asked:** when Rook is asked to look and the vision server on DESKTOP-2 isn't running, she should say she's pulling it up, start it, wait, then look.

**Done:**
- New `projects/Rook/Rook-Vision/vision_launcher.py` (port 8766, `/status` and `/start`, optional `X-Rook-Token`, 60s cooldown, log `launcher_log.txt`). It can only run `Start_Vision_Server.bat`.
- New `Install_Launcher_Startup.bat` (Startup shortcut using `pythonw.exe`, starts the launcher now and at every login). `Open_Firewall.bat` now also opens 8766. README Stage 6 added. `launcher_log.txt` in `.gitignore`.
- Main PC `Rook\rook_eyes.py`: `answer(text, say=None)` now calls `_ensure_server(say)` first (health check on `remote_url`, then says "Pulling up the vision system, one moment.", asks the launcher to start, polls up to 120s). Spoken failures: can't reach the vision computer / couldn't start / didn't come up in time. `Rook\rook.py` passes `say=rook_says`. Backups in `Rook\backups\` (`rook_eyes_backup_before_autostart.py`, `rook_backup_before_eyes_autostart.py`). These Rook files are outside the repo.

**Untested / open:** everything above. The earlier shorter-answer tests are still pending too. The main PC clone and DESKTOP-2 both need `git pull`.

**Things to test**
1. DESKTOP-2: `git pull` in `Desktop\Claude`. Run `Open_Firewall.bat` as administrator (port 8766). Run `Install_Launcher_Startup.bat` once.
2. From the main PC browser open `http://<DESKTOP-2 IP>:8766/status`; expect `{"launcher": true, "server_up": ...}`.
3. Close the vision server window (and LM Studio server if you like). Restart Rook on the main PC, ask "can you see me". Expect "Let me take a look.", then "Pulling up the vision system, one moment.", then an answer. Check `rook_eyes_log.txt` and `launcher_log.txt`.
4. With the server already running, ask again: no "pulling it up" line.
5. Turn DESKTOP-2 off or stop the launcher and ask: expect "I can't reach the vision computer."
6. Then the shorter-answer tests from the previous section.


## 2026-10-27 (main PC session, 17:10) - on-demand start tested OK; Rook now stops the vision server on exit

**Tested OK (user):** with the server off, Rook said she was pulling it up; server was up after 14s, first look 6.5s total. Four looks with the shorter answers: 6.5 / 6.1 / 6.0 / 6.0s (model 3.6-4.1s, camera 2.3s), down from 8-11s.

**Asked:** Rook should shut the vision server down when she shuts down.

**Done:** `vision_launcher.py` gained `POST /stop` (kills the server window/process tree, anything still listening on 8765, then `lms unload --all`). Main PC `Rook\rook_eyes.py` registers an `atexit` hook that calls `/stop`, only if Rook started the server this session (so a hand-started server is left alone). Backup: `Rook\backups\rook_eyes_backup_before_shutdown_hook.py`. Limits: does not run if Rook's window is force-killed or the PC crashes.

**Things to test**
1. DESKTOP-2: `git pull`, then restart the launcher (end the pythonw.exe process in Task Manager, or sign out/in, then run `Install_Launcher_Startup.bat` again) so it loads `/stop`.
2. Main PC: restart Rook, server off. Ask "can you see me" (she pulls it up), then close Rook normally. Expect the server window to close, and LM Studio to show no loaded model. Check `rook_eyes_log.txt` for "asked the launcher to stop" and `launcher_log.txt`.
3. Start the server by hand, start Rook, ask her to look, close Rook: the server should stay running.
4. Close Rook by clicking the window X and note whether the server stops (it may not).
