# START HERE (Claude-HQ)

This repo is the shared oversight hub for all projects. Both PCs keep a clone of it.
Main PC: DESKTOP-1 (C:\Users\cheye\Desktop\Claude) | 2nd PC: DESKTOP-2 (C:\Users\Cheyenne\Desktop\Claude)

## Session start (every new chat)
1. `git pull` in this folder first (the other PC may have pushed).
2. Read this file, then the matching note in `Handoffs/` (Rook.md, TradeBot.md, Skills.md or Misc.md). Read the LAST section of that note first.
3. Only access the PC the task needs.

## Session end (or when asked)
1. Append a dated section at the bottom of the matching `Handoffs/` file: what was asked, what was done, what's untested or open, and a numbered "Things to test" list if anything changed.
2. Brand-new project: create a project folder under `projects/` and a new dated file in `Handoffs/`, and add it to the layout below.
3. Check the file's size and modified time right before editing (another session may be appending).
4. `git add -A && git commit -m "<what changed>" && git push`.
5. If folders or files move, update the layout below.

## Layout
- `START-HERE.md` - this file
- `Handoffs/` - one running note per area: Rook.md, TradeBot.md, Skills.md, Misc.md
- `projects/Rook/` - Rook voice assistant; `Rook-Vision/` = camera + local vision AI (runs on DESKTOP-2)
- `projects/TradeBot/` - Alpaca paper-account stock watcher
- `.gitignore` - keeps venvs, snapshots, results, secrets out of git

## Rules
- Never commit secrets (API keys, tokens, Alpaca keys, `.env`). Keep them local and gitignored.
- Handoff notes are append-only; add new dated sections at the bottom.
- When Claude changes something to be tested, end the update with a short numbered "Things to test" list.
