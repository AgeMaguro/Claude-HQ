# Skills handoff notes

Append dated sections at the bottom. Newest last.

## Imported history from the old Claude folder (merged 2026-10-27, main PC)

Everything below was copied word for word from the old `Claude\Handoffs\Skills.md` (that folder is now `claude-old` on the main PC), in its original order, oldest first. Paths inside these sections use the old layout; see START-HERE.md for where things live now.

Split out of `Claude_handoff.md` on 2026-10-12. Section text is copied word for word, in its original order (oldest first). The original file is kept in `Archive\`.

## Contents

1. Handoff: Skills folder, video-learning (sessions of 2026-10-11 evening)

---

## Handoff: Skills folder, video-learning (sessions of 2026-10-11 evening)

Three notes merged in the order they happened: (1) tool setup, (2) first video study, (3) comedy editing study. The folder is `Claude Handoff\Skills\` and its rules live in its own `CLAUDE.md` and `AGENTS.md`. Styles so far: `short-form` (18 rules after the first study) and `long-form` (20 rules, 8 confirmed).

### Tool setup (cloud chat linked to the PC, 2026-10-11 about 8:05 to 8:45 pm US Central)

Covers only the setup chat. The video studies follow in this same section.

#### What was asked and built
- The user pasted a prompt: build a folder that teaches Claude a skill (editing, hooks, design) from videos, with Agent-Reach, claude-video (`/watch`) and a free Gemini key.
- Built `Claude Handoff\Skills\` as specified (CLAUDE.md, AGENTS.md, Input, Sessions, Workspace with Templates/Research/AI-Only, Output) with one style, `short-form`. The prompt's `CHANGELOG.mg` was made `CHANGELOG.md`. CLAUDE.md holds the user's reading prompt word for word.
- The cloud workspace could not reach YouTube, GitHub or PyPI (proxy 403), so nothing could be installed or watched from there. All installs were done by the user on their PC. `/watch` only works in a local Claude Code session (Code tab, `</>` button, Local, folder `Desktop\Claude Handoff\Skills`), not in a cloud chat.

#### Fixes for errors in the original prompt (so they are not repeated)
- Agent-Reach: the PyPI package `agent-reach` is a different project. Install from GitHub: `pip uninstall agent-reach -y`, then `pip install https://github.com/Panniantong/Agent-Reach/archive/main.zip`. Then `agent-reach install --env=auto --safe` (the URL form in the prompt gives "no channel named ..."). Check with `agent-reach doctor` (output is in Chinese). Result: 5 of 16 channels work, including YouTube video info and subtitles. Not set up: Instagram, X, Reddit and the other login channels, `gh` CLI, and Exa search (needs `npm install -g mcporter` and `mcporter config add exa https://mcp.exa.ai/mcp --scope home`). There is no TikTok channel, so TikTok goes through yt-dlp.
- claude-video: the repo is `bradautomates/claude-video` (the prompt had `jbradautomates`). Needs Python 3.10+, ffmpeg, yt-dlp and Deno (winget: Gyan.FFmpeg, yt-dlp.yt-dlp, DenoLand.Deno). `/plugin marketplace add` was not available inside the desktop app, but the `watch` plugin still showed up as a skill and worked in the local Code session.
- Gemini key: the right page is aistudio.google.com/apikey (the prompt had a typo). New keys start with `AQ.` and are 53 characters, not `AIza`. The user tested theirs with the models-list curl call and it worked. Key lives in `Skills\Workspace\AI-Only\tools\.env` and is read in place by `/watch`.

#### Open items
- The Gemini key was shown in the chat (an attached terminal log). The user was told they can make a new key later and replace it in `.env` (and in `~\.config\watch\.env` if it was copied there). Not done yet.
- The Gemini key later hit its quota (see the comedy editing section above).
- Optional channels (Instagram etc.), `gh`, and Exa search are still not installed.
- RUNBOOK.md in `Skills\Workspace\AI-Only\` has the status checklist; the cloud-side note there about the key format was corrected.

#### Reminders
- This cloud session needed fresh folder approval for `Claude Handoff` (device_request_folder_access); a new session will need it again.
- User preference: handoff notes go in this file; end updates with a numbered "things to test" list when a change needs testing (nothing in this setup needs testing).

### First video study (session of 2026-10-11 evening)

#### What was done
- Job `Sessions/2026-10-11_first-video` finished. The frozen RULES/CHANGELOG copies in the session folder were left untouched.
- `/watch` set up for the first time: local engine, default detail = transcript (both the user's choice), WhisperX transcription. For this job the user OK'd frames for the TikTok plus the YouTube opening and cue moments.
- Beat timelines: `Skills/Workspace/Research/watched/tiktok_7674567872319966477.md` and `youtube_tREcxG_UouI.md`.
- 18 rules added to the live template `Skills/Workspace/Templates/short-form/RULES.md` (1 confirmed: "make the video its own proof"; 17 from one video each). All are logged in its CHANGELOG.
- Output: `Skills/Output/2026-10-11_first-video_study.md`.

#### Things to know
- The YouTube link is a 33-min Vegas Pro tutorial (long-form), not a short. Only the TikTok is real short-form, so the hook and design rules rest on one short.
- WhisperX needed a workaround because the Claude app's MSIX sandbox redirects AppData. The fix is written up in `Skills/Workspace/AI-Only/RUNBOOK.md`.
- TikTok frames were sampled on scene changes only (18 frames), which left gaps at 0:19–0:29 and 0:35–0:42.

#### Open items
- Next job: 2–3 more talking-head + graphics shorts, to confirm or drop the 17 one-video rules.
- Optional: rewatch the TikTok at `--fps 1` to get the real cut rate.
- No corrections from the user yet.

### Comedy editing study (session of 2026-10-11, late evening)

#### What was done
- Logged the user's long-form channels SMii7Y and SovietWomble in `Skills/Workspace/Research/sources.md`, with the user's reason in their words: "the editing, the humor and timing of edits and jokes, the subtitle edits".
- Created a separate `long-form` style: `Skills/Workspace/Templates/long-form/`.
- Job `Sessions/2026-10-11_comedy-editing` finished: 4 videos (2 per channel). Each gets transcripts plus my own frames for selected windows, and SovietWomble also got Gemini audio passes. The user chose option 2: Gemini reads the key in place from tools/.env.
- 20 long-form rules (8 confirmed). Output: `Skills/Output/2026-10-11_comedy-editing_study.md`.

#### Open items
- Gemini key hit its quota (HTTP 429), so neither SMii7Y video has audio analysis. When it resets, rerun the windows listed in the Output file, one at a time.
- The short-form search from earlier is paused: 5 candidate Shorts are listed in this session's chat (Sabrina Ramonov, Greg Isenberg, Nick Automates, GrowthX, KodeKloud), not yet checked for style.
