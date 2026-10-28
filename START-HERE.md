# START HERE (Claude-HQ)

This repo is the shared oversight hub for all projects. Both PCs keep a clone of it.
Main PC: DESKTOP-1 (C:\Users\cheye\Desktop\Claude) | 2nd PC: DESKTOP-2 (C:\Users\Cheyenne\Desktop\Claude)

This folder was called "Claude Handoff" until 2026-10-12. Older notes still say "Claude Handoff"; it is the same folder (now this git repo). The pre-repo copy of the main PC's folder is kept as `Desktop\claude-old` (outside git).

## Session start (every new chat)
1. `git pull` in this folder first (the other PC may have pushed).
2. Read this file, then the matching note in `Handoffs/` (Rook.md, TradeBot.md, Skills.md, Misc.md, Productivity.md or the RimWorld file). Read the LAST section of that note first.
3. Only access the PC the task needs.

## Session end (or when asked)
1. Append a dated section at the bottom of the matching `Handoffs/` file: what was asked, what was done, what's untested or open, and a numbered "Things to test" list if anything changed.
2. Brand-new project: create a project folder under `projects/` and a new dated file in `Handoffs/`, and add it to the layout below.
3. Check the file's size and modified time right before editing (another session may be appending).
4. `git add -A && git commit -m "<what changed>" && git push`.
5. If folders or files move, update the layout below.

## Layout
- `START-HERE.md` - this file
- `Handoffs/` - one running note per area, newest section last. Rook.md, TradeBot.md, Skills.md and Misc.md also hold the old pre-repo history (the "Imported history" section, merged 2026-10-27, oldest first):
  - `Rook.md` - voice assistant: main handoff, Quest 3, webcam, workshop mode, Orbit sphere, weather, desktop skills, Discord, Rook-Vision (incl. Stage 5 remote camera on the 2nd PC)
  - `TradeBot.md` - TradeBot and TradeBot-GPU (v0.01 to v0.37), restart menu, phone alerts, day-trade brainstorm
  - `Skills.md` - video-learning skills folder
  - `Misc.md` - 2FA in KeePassXC, PokeAPI/TwitchIO, God's Eye View, Python versions, folder cleanup and rename
  - `Productivity.md` - Productivity plugin setup (tasks, memory, dashboard)
  - `2026-10-24_RimWorld-test-mod.md` - RimWorld test mods: XML mod (Hearth Lantern, Trail Biscuit) and Harmony/HugsLib C# patch mod; both live in the game's `Mods\` as `ClaudeTest_HearthAndBiscuit` and `ClaudeTest_CrunchPatch`; session 2 has the C# build recipe; session 3 is the colony tracker mod (`ClaudeTest_ColonyTracker`)
  - `2026-10-28_Dragonwilds-server.md` - RuneScape: Dragonwilds dedicated server on DESKTOP-2: config path, ports (UDP 7777), Vilo port forwarding, launcher .bat, and the 16-character name truncation that hid it from the browser (search `Forsaken Dragonw`)
- `projects/Rook/` - Rook voice assistant; `Rook-Vision/` = EMEET Pixy camera + local vision model so Rook can see (scripts, `README.md` with the stages). Old notes call it `Rook-Vision\`. Hooked into Rook via `Rook\rook_eyes.py` (2026-10-13, tested working by the user). Stage 5 (2026-10-27): camera + LM Studio can live on the 2nd PC via `vision_server.py` and `remote_url` in `config.json`; see its README. Notes: last section of `Handoffs/Rook.md`.
- `projects/TradeBot/` - Alpaca paper-account stock watcher (code not moved into the repo yet; see below)
- `.gitignore` - keeps venvs, backups, snapshots, results, `.env` and keys out of git

### Still outside the repo (main PC, in `Desktop\claude-old`; old notes call these `Claude\<name>`)
- `TradeBot-GPU\` - the live trading app (current version in the last section of `Handoffs/TradeBot.md`). Its `.env` holds API keys: never commit it.
- `Skills\` - video-learning workspace (has its own `CLAUDE.md` and `AGENTS.md`; read those first for any Skills job)
- `RimWorld-Tracker\` - external colony tracker window for RimWorld (`tracker.py`, `Run_Tracker.bat`, `Run_Tracker_Demo.bat`; reads the JSON written by the ClaudeTest_ColonyTracker mod). Notes: `Handoffs/2026-10-24_RimWorld-test-mod.md`
- `Rook\` - Rook extras (`orbit-menu.html`). The main Rook program is on the Desktop in `Rook`, and its notes are in `Documents\GitHub\Rook-vault`.
- `Productivity\` - Productivity plugin files: `TASKS.md` (task list), `dashboard.html` (open in a browser). `CLAUDE.md` is the short working memory (people, projects, terms); `memory\` for the full glossary is not created yet.
- `Archive\` - old copies: previous versions of the handoff file, the old `TradeBot` v1 folders, older code backups. Nothing here is needed day to day.

## Rules
- Never commit secrets (API keys, tokens, Alpaca keys, `.env`). Keep them local and gitignored. Never print API keys; they live in `.env` files.
- Paper trading only (Alpaca paper account).
- Back up to `backups\` before editing code (`backups/` is gitignored).
- Handoff notes are append-only; add new dated sections at the bottom.
- When Claude changes something to be tested, end the update with a short numbered "Things to test" list.
- File-copy gotcha: after `device_commit_files`, wait about 8 seconds and compare md5sum of the PC file with the staged one; commit again if they differ.
- Start a new chat per feature to save usage.
