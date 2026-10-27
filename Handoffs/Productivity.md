# Productivity plugin handoff

_Copied word for word from the old `Claude\Handoffs\Productivity.md` on 2026-10-27 (main PC). Append new dated sections at the bottom, newest last._

## Handoff: Productivity first-time setup (2026-10-12, about 3:45 to 4:10 pm US Central)

### What was asked
"Get me started with Productivity" (the /productivity:start flow).

### What was done
- Created `Productivity\` in the Claude folder and put two files in it: `TASKS.md` (empty template: Active, Waiting On, Someday, Done) and `dashboard.html` (the plugin's task and memory dashboard). md5 checked after copying; both match.
- Added `Productivity\` and this note to the layout in START-HERE.md.

### Not done / open
- Memory bootstrap not started. `CLAUDE.md` and `memory\` do not exist yet. Next step: user says where their todos live (a file, app, or notes) so shorthand, names and project codenames can be decoded and written to `Productivity\CLAUDE.md` and `Productivity\memory\`.
- Optional comprehensive scan of messages, email and docs was offered but not chosen.
- Dashboard not opened yet; the user opens it from the file browser.

### Things to test
1. Open `Desktop\Claude\Productivity\dashboard.html` in a browser and check the task board loads.
2. Add a test task in the dashboard, then check it appears in `TASKS.md`.

## Update: tasks seeded from handoff notes (2026-10-12, about 3:50 pm US Central)

### What was asked
User said to use the handoff notes as the to-do list source for the memory bootstrap.

### What was done
- Read open items, "Not done", "Still open" and "Things to test" sections of Rook.md, TradeBot.md, Skills.md and Misc.md.
- Filled `Productivity\TASKS.md`: Active (tests and next steps by project), Waiting On (undecided choices), Someday (ideas).
- Wrote `Productivity\CLAUDE.md` (projects, terms, preferences). Name and role left blank on purpose; not stated by the user.

### Not done / open
- `Productivity\memory\` (full glossary, people, project files) not created.
- Task list built from notes only; user has not yet reviewed it. Some items may already be done.
- No comprehensive scan of email/chat/docs.

### Things to test
1. Open `Productivity\dashboard.html` and check the tasks show in Active / Waiting On / Someday.
2. Tell Claude anything wrong or already done so TASKS.md can be pruned.
