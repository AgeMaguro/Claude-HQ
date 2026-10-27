# Misc handoff notes

Append dated sections at the bottom. Newest last.

## Imported history from the old Claude folder (merged 2026-10-27, main PC)

Everything below was copied word for word from the old `Claude\Handoffs\Misc.md` (that folder is now `claude-old` on the main PC), in its original order, oldest first. Paths inside these sections use the old layout; see START-HERE.md for where things live now.

Split out of `Claude_handoff.md` on 2026-10-12. Section text is copied word for word, in its original order (oldest first). The original file is kept in `Archive\`.

## Contents

1. Handoff note: moving Google Authenticator codes to KeePassXC
2. Handoff Note: Learning APIs, PokéAPI and TwitchIO
3. Handoff: God's Eye View chat (2026-10-11)
4. Note: multiple Python versions on this PC (2026-10-11, saved for later)
5. Folder cleanup and rename to Claude (2026-10-12)

---

<!-- source file: handoff-2026-10-11-2fa-keepassxc.md -->

## Handoff note: moving Google Authenticator codes to KeePassXC

Date: 2026-10-11

### Goal
Mirror Google Authenticator codes on the PC using a free, local, private option.

### Decision
- Using **KeePassXC** (free, open source, offline, Windows) to store TOTP codes.
- Considered and set aside: Authy (desktop app discontinued), Bitwarden/1Password (paid), WinAuth (older, less maintained).

### What was done
- Wrote an offline script, `ga_export_decoder.py`, that decodes the Google Authenticator "Export accounts" QR screenshot into each account's issuer, name, base32 secret and otpauth:// URI. No network calls. Only dependency: `pip install opencv-python`.
- Tested on a sample QR (image and `--url` input); output was correct. Not yet tested on Windows by Claude.
- Run it with: `python ga_export_decoder.py export.png` (use `py` if `python` isn't recognized; multiple QR images can be passed in one command).
- First account set up in KeePassXC: Entries > New Entry, then right-click > TOTP > Set up TOTP, paste the Secret, keep defaults (SHA1, 6 digits, 30 s). Ctrl+T copies the current code.
- First attempt didn't match the phone. PC clock was fixed (Settings > Time & language > Date & time > Sync now). The code then matched.

### Daily use (confirmed with user)
- Open KeePassXC, open the database, enter the master password.
- Select the account's entry, then press Ctrl+T to copy the current code (or right-click > TOTP > Show TOTP).
- Codes last 30 seconds, so copy right before use. Lock the database with Ctrl+L when done.

### Handoff delivery
- The PC was off earlier, so this note could not be saved to the Claude Handoff folder then. It was sent as a file in chat; this updated version should be saved to `C:\Users\cheye\Desktop\Claude Handoff`.

### Still to do
- Set up the remaining accounts and verify each against the phone before removing anything.
- Keep Google Authenticator on the phone until every account matches.
- Back up the .kdbx file to a separate location (e.g. USB drive).
- Save each site's backup codes.
- Clean up: delete the QR screenshot, clear the terminal output, empty the Recycle Bin. Don't paste secrets anywhere online.

### Notes
- If a code doesn't match: check PC clock, re-paste the secret (no label or spaces), confirm the right account, and confirm the digits/algorithm from the URI line.
- Optional idea offered: add a `--code` flag to the script that prints the current code per account, to separate secret problems from KeePassXC problems.

---

<!-- source file: handoff-2026-10-11-apis-pokeapi-twitchio.md -->

## Handoff Note: Learning APIs, PokéAPI and TwitchIO

Date: Sunday, October 11, 2026
Topic: Beginner coding education (no project files changed)

### Where things stand
The user has next to no coding experience and wants to learn at a pace that fits a working adult's schedule. This conversation was pure learning and Q&A. Nothing was built, installed or modified.

### What we covered
1. **Benefits of public APIs:** saves time, often free to start, maintained by the provider, standardized (REST/JSON), easy to combine. Tradeoffs: rate limits, pricing changes, third-party uptime, keeping API keys secret.
2. **Suggested learning path:** 15-20 minutes a day, learn the basic idea of an API first, pick one beginner language (Python), build one tiny project, start with free no-key APIs.
3. **PokéAPI:** free, no key needed. Example: `https://pokeapi.co/api/v2/pokemon/pikachu` returns JSON in the browser. A 3-line Python `requests` example was shown.
4. **Twitch Pokémon chat games:** typically a chat bot + PokéAPI + small database + stream overlay. Different from *Twitch Plays Pokémon*, which turned chat into controller inputs.
5. **TwitchIO:** async Python library for Twitch chat bots (chat connection, commands, events, Twitch API access, EventSub).
   - Version caveat: 2.x is the older style most tutorials use. 3.x is a newer rewrite with different setup (docs at twitchio.dev). The current stable version was NOT confirmed, so check twitchio.dev before installing and match tutorials to the version.
6. **Code walkthrough:** the user explained the example bot in their own words and was close. Corrections given:
   - `commands` is a toolkit that includes the `Bot` class.
   - The class is a blueprint that inherits TwitchIO's abilities.
   - `__init__` is the one-time setup step; `super().__init__(...)` passes settings to the parent class.
   - The prefix (`!`) only marks a command; the command name comes from the function name (`def catch` means `!catch`).
   - `async`/`await` lets the bot do other things while waiting.
   - `ctx` holds the command details, including the sender.

### Suggested next steps
- Try the exercise: rename `hello` to `catch` and make it reply with a Pokémon name.
- Run the simple PokéAPI Python script first, before adding a Twitch bot.
- Install Python and make a first working script.
- When ready for a bot, create a Twitch account/token and check twitchio.dev for the current version's quickstart.

### Open questions
- Which TwitchIO version is current stable (unconfirmed).
- Whether the user wants a Twitch bot specifically or just general API practice.

---

<!-- source file: handoff-2026-10-11-gods-eye-view.md -->

## Handoff: God's Eye View chat (2026-10-11)

### What this chat covered
- User asked what the "god's eye view" is. Gave the general meaning: top-down or omniscient vantage point (games, writing/film, general overview).
- User said there is supposedly an app that taps into real-time data. Searched the web and identified the likely match.

### Likely app: God's Eye View (formerly WorldView)
- Open-source project by Bilawal Sidhu, MIT license. Repo: github.com/bilawalsidhu/gods-eye-view
- Browser-based, built on CesiumJS. Photorealistic 3D globe with about 13 live layers: flights, military flights, ships, satellites, earthquakes, traffic, public cameras, radio, fires, launches.
- Voice control and analyst-style queries (uses the OpenAI Realtime API).
- Cockpit mode rides along with a live aircraft, with sensor looks like thermal and night vision.
- Most layers need no API keys or account. Optional keys go in the in-app Provider Settings panel.
- Data sources: OpenSky and adsb.lol (flights), CelesTrak (satellites), USGS (earthquakes), AISStream (ships).
- Caveats: not a literal spy satellite feed. Some layers are delayed, simulated, cached or estimated. Real-time data has about 10+ seconds of latency.
- To run it: clone the repo, then `npm run dev` (Node.js). Also packaged for Unraid and Pinokio.
- Possible mix-up: a separate, smaller project called "God Mode View" (github.com/jastfan/god-mode-view) also exists.

### Open items
- User has not confirmed this is the app they meant. If not, ask where they heard about it.
- User has not said whether they want to install or run it.

### Things to test
None. No code or project files were changed in this chat.

---

## Note: multiple Python versions on this PC (2026-10-11, saved for later)

- On 2026-10-11 TradeBot GPU failed to start with `ModuleNotFoundError: No module named 'pandas'`. Cause (user's own explanation): another project made them install a different Python version, so `python` now points at a fresh install with none of the libraries. Nothing was broken; the old Python still has its libraries.
- Options explained to the user: (1) run `Install_Requirements.bat` (uses `python -m pip`, so it installs for the same `python` the run script uses; may fail if the new Python is too new for prebuilt packages), (2) change the run scripts to pick a version with the `py` launcher (`py -0` lists installs, e.g. `py -3.12 tradebot_gpu.py`), (3) create a per-project virtual environment (venv) via a one-click script. Option 3 is the most robust if Python versions keep changing; option 2 or 3 avoids disturbing the other project.
- Not decided or done yet. To resume: ask the user for the output of `py -0` and whether the install bat worked.

---

## Handoff: Folder cleanup and rename to Claude (2026-10-12, about 3:35 to 4:00 pm US Central)

### What was done
- The user renamed Desktop\Claude Handoff to Desktop\Claude themselves (a session cannot rename its own connected folder). An empty Desktop\Claude Handoff folder was left behind; safe to delete.
- Claude_handoff.md (105 KB) was split word for word into Handoffs\Rook.md, TradeBot.md, Skills.md, Misc.md; checked line by line that nothing was lost. The phone-alerts note was merged into TradeBot.md. Claude_handoff.md at the top is now a short pointer to START-HERE.md.
- New START-HERE.md: folder map and the standing rules (paper only, no keys printed, backups before edits, numbered "Things to test", md5 check after commits).
- Archive\ holds: old-handoff-files (original combined file, four .bak copies, phone-alerts note), old-TradeBot-folders (TradeBot v1 and TradeBot_v1.43_backup), TradeBot-GPU-older-backups (41 older code backups; the newest 2 per file stay in TradeBot-GPU\backups), and pre-cleanup-2026-10-12 (a full copy of the notes as they were before cleanup; safe to delete once the user is happy).
- orbit-menu.html moved to Rook\; the three lines in Rook.md that named its location were updated. Skills\CLAUDE.md now points at the Claude folder and START-HERE.md.
- __pycache__ folders deleted (Python rebuilds them). No TradeBot code was changed.

### Not done / open
- The user's Instructions for Claude setting may still say "Claude Handoff"; the user edits that themselves.
- Older sections still mention backup file names that now live in Archive\TradeBot-GPU-older-backups.
- Not touched: TradeBot-GPU stays where it is (shortcuts or scheduled tasks may point at it).

## 2026-10-27 (main PC) - old handoff history merged into Claude-HQ
Asked: read the old `Claude-old\` notes (START-HERE.md and everything in Handoffs), merge their history into this repo's Handoffs\, merge the old layout/rules into START-HERE.md (keeping the git pull/push steps), no secrets, commit and push.
Done:
- Appended the full old Rook.md, TradeBot.md, Skills.md and Misc.md below each file's existing content, word for word, in original order, under an "Imported history from the old Claude folder" heading. The 2026-10-27 Claude-HQ entry in Rook.md stays above it.
- Copied the two old notes with no counterpart here as their own files: `Productivity.md` and `2026-10-24_RimWorld-test-mod.md`.
- START-HERE.md: kept the git pull/push steps; added the old layout descriptions (Handoffs files, Rook-Vision stages, folders still outside the repo) and the old rules (paper trading only, back up to backups\ before editing code, file-copy md5 gotcha, new chat per feature).
- Not copied: `Archive\`, `TradeBot.md.bak`, old `Claude_handoff.md` pointer, and all code/data folders (TradeBot-GPU has a `.env` with keys). A scan of the merged notes found no keys or tokens.
- The PC sandbox cannot reach github.com (403 from proxy), so the commit was pushed from the cloud session instead.
Open:
- TradeBot-GPU, Skills, RimWorld-Tracker, Productivity and Rook\orbit-menu.html still live only in `Desktop\claude-old` on the main PC, not in the repo.
- Old notes use old paths (`Rook-Vision\` is now `projects\Rook\Rook-Vision`; the live Rook code is on the Desktop in `Rook`).
- Several files on the main PC clone show as modified from Windows line endings only (CRLF vs LF); untouched by this commit.
- The Instructions-for-Claude setting still needs the new workflow (git pull first, push at end).
Things to test:
1. Main PC: `git status`; if the merged files show as modified, run `git checkout -- START-HERE.md Handoffs` then `git pull`.
2. DESKTOP-2: `git pull`, then open START-HERE.md and Handoffs\Rook.md and confirm the imported history is there.
3. Skim the end of Handoffs\TradeBot.md for the latest version (v0.37) and confirm it matches what you remember.
