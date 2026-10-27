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
