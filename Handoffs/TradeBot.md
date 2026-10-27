# TradeBot handoff notes

Append dated sections at the bottom. Newest last.

## Imported history from the old Claude folder (merged 2026-10-27, main PC)

Everything below was copied word for word from the old `Claude\Handoffs\TradeBot.md` (that folder is now `claude-old` on the main PC), in its original order, oldest first. Paths inside these sections use the old layout; see START-HERE.md for where things live now.

Split out of `Claude_handoff.md` on 2026-10-12. Section text is copied word for word, in its original order (oldest first). The original file is kept in `Archive\`.

## Contents

1. Handoff: Day-trade checker bot brainstorm (chat started 2026-10-08)
2. Handoff: Stock ticker app, GPU rewrite (session of 2026-10-11)
3. TradeBot GPU: v0.08 to v0.17 (2026-10-11)
4. TradeBot: Restart menu (v0.18) and phone-alert watcher (watch.py) (2026-10-12, morning; follows a phone chat the night before)
5. Addendum - console window fix (2026-10-12)
6. Addendum - restart fix v0.23 and icon v0.24 (2026-10-12)
7. Addendum - icon redesign (2026-10-12)
8. Addendum - Rook chat box v0.25 (2026-10-12)
9. Addendum - Rook v0.26 (2026-10-12)
10. Addendum - v0.27 (2026-10-12)
11. Addendum - v0.28: font size, intraday time axis, range-for-Rook (2026-10-12)
12. Addendum - v0.29 tooltip fix (2026-10-12)
13. Addendum - v0.30 overlays on 15-minute candles (2026-10-12)
14. Addendum - v0.31 (2026-10-12)
15. Addendum v0.32 - Rook's sphere and voice (TradeBot-GPU)
16. Handoff - end of session 2026-10-12 (TradeBot-GPU v0.32)
17. Handoff: TradeBot headless + phone alerts (2026-10-11)

---

<!-- source file: handoff-2026-10-11-day-trading-bot-brainstorm.md -->

## Handoff: Day-trade checker bot brainstorm (chat started 2026-10-08)

### What this chat covered
Brainstorming and learning only. No code or project files were created or changed.

### The idea
User wants to build a bot to "check day trades." Three versions were offered:
1. **Rule tracker:** counts day trades in a rolling 5-business-day window and warns before hitting pattern-day-trader (PDT) or margin limits. FINRA has been revising PDT rules, so confirm current thresholds before coding them.
2. **Trade reviewer / journal bot:** pulls executed trades after the close and grades them (win rate, average R, slippage, holding time, rule breaks like sizing or stops). Best fit for learning and improving.
3. **Setup checker:** checks a ticker against entry criteria (relative volume, spread, VWAP position, news, float) before entering.

Shared parts: broker API or CSV export of fills (Alpaca, Schwab, IBKR, Tradier); Python + pandas; output to Discord/Telegram, email or a small dashboard. Recommended keeping it **read-only** at first (watch and report, never place orders).

### Trading education covered
- Most day traders lose money over time, so learn, paper trade and track yourself first.
- Foundations: risk management (small fixed risk per trade, e.g. 1%, always a stop, size from stop distance), order types, slippage and spreads, chart reading, settlement/margin/PDT, short-term capital gains tax.
- Common strategies: momentum/gap-and-go, breakouts, VWAP trading, pullbacks in a trend, mean reversion (riskier for beginners).
- What to watch: relative volume, catalysts (earnings, news, CPI, Fed days), spread and liquidity, overall market context, own behavior (revenge trading, overtrading, moving stops).
- Learning path: pick one strategy with exact rules, paper trade for a few weeks (e.g. Alpaca free paper account), log every trade (where the journal bot fits), only then consider small real money.
- Resources: Investopedia, broker education sections, *Trading in the Zone* (Mark Douglas).
- Framed as education, not financial advice.

### Where it was left
User said they were just curious for now and their brain was tired. Nothing decided.

### Open questions for next time
- Which bot version they want (tracker, reviewer or setup checker).
- Which broker they use. (Not confirmed in chat; the PC has a thinkorswim folder, which would point to Schwab, but ask before assuming.)
- Whether they want to go deeper on one strategy or start with a paper-trading journal bot.

### Things to test
None. No code or project files were changed in this chat.

---

## Handoff: Stock ticker app, GPU rewrite (session of 2026-10-11)

### Where things are
- `TradeBot\` = the original Tkinter app, final version 1.43 (stock watchlist, scoring, charts, chart grid, Alpaca PAPER trade tab, settings menu, perf logging). Untouched. `TradeBot_v1.43_backup\` is a full copy of it.
- `TradeBot-GPU\` = new Qt (PySide6) version, "TradeBot GPU - Version 0.01". Charts are drawn on the graphics card via OpenGL. Not yet run on real hardware.

### Why
Tk panning was stuck near 30 fps because the app was bound to one CPU core (perf CSV: 90-98% of one core). Threads can't fix that (Python GIL, Tk main-thread only), so the drawing moved to Qt/GPU.

### GPU project files
- `core.py`: no window code. Colours/themes, DataStore (cache.json, settings, background refresh/hourly threads), ChartModel (builds a list of draw ops; tested here against real cache data), GridModel.
- `qt_widgets.py`: ChartWidget/GridWidget (QOpenGLWidget + QPainter, 4x MSAA; plain QWidget in safe mode). `qt_theme.py`: style sheet (rounded gradient bevel buttons, tabs). `trade_qt.py`: Trade tab (paper only, every order/cancel/close confirmed). `tradebot_gpu.py`: main window, menus, 500 ms tooltips.
- Run with `Run_TradeBot_GPU.bat`; `Run_TradeBot_GPU_Safe.bat` forces CPU drawing. First run `Install_Requirements.bat`.
- Logs: `tradebot_gpu_log.txt` (errors, startup renderer), `tradebot_gpu_perf.csv` (CPU/GPU/ui lag per second with activity tags).

### Rules / preferences
- Trading stays paper-only (hard-coded, account must start with PA). `.env` holds the paper keys: never print or paste them.
- Version in the title bar, tick up 0.01 per change. End updates with a numbered "Things to test" list.

### Not done / next
- First real run of the Qt app will likely surface bugs (it could only be checked with stubs here). Send `tradebot_gpu_log.txt` and screenshots.
- Compare panning: perf CSV for old vs new.
- Options trading not built (offered). Old app has no further planned changes.

### Update (same day, later): TradeBot GPU is at version 0.06 and working
- User confirmed panning, zooming and scrolling are smooth on the GPU version; layout and corners look right.
- Fixes since 0.01: the app now loads the Alpaca keys from `.env` (`tradebot.load_env()` is called in `core.py`); buttons and tabs are hand-drawn bevelled widgets (`BevelButton`, `BevelTabBar` in `qt_widgets.py`); range buttons (1M..Max) sit under the tabs; watchlist and chart are separated by a draggable splitter (position saved in `gui_settings.json`); chart corners fill with the colour sampled from behind the widget (`probe_corner`), because transparent corners rendered black with OpenGL.
- Safe mode (`Run_TradeBot_GPU_Safe.bat`) draws on the CPU and had clean corners all along.
- Next ideas: options trading on the Trade tab (not built), compare perf CSV old vs new, retire the old Tk app when happy.

### Update: TradeBot GPU 0.07 adds options (confirmed working by user)
- Trade tab has Instrument = Stock / Option. Option flow: "Load contracts" (60 days, strikes within 20% of price) -> call/put, expiry, strike -> bid/ask/mid fetched, limit prefilled -> Review -> confirm -> paper order (Limit/Market, Day, whole contracts). Code: `option_contracts`, `option_quote`, `submit_option`, `validate_option`, `describe_option` in `broker.py`; UI in `trade_qt.py`.
- Still paper-only with confirmation on every order. Not built: multi-leg strategies (spreads), exercising options, options in the chart/score.

---

## TradeBot GPU: v0.08 to v0.17 (2026-10-11)

Project folder: `TradeBot-GPU` (PySide6/Qt, Alpaca PAPER only; every order behind a confirmation dialog; `.env` holds paper keys, never print them). Old Tkinter version is untouched in `TradeBot` / `TradeBot_v1.43_backup`. Title bar shows the version; it ticks up 0.01 per change.

#### Added since v0.07
- **Chart overlays** (checkboxes): Bollinger bands, MACD crosses, golden/death cross, earnings dates (with EPS surprise), expected move (options-implied range, shaded, no longer stretches the chart), my option positions (strike and break-even lines). Work on daily and hourly (1M) views. Legend notes when no cross is in view.
- **History** fetched at 1000+ days; prices are split-adjusted (fixed NFLX 10:1 showing -91%).
- **Strategies tab**: plain-language signals now plus a backtest of golden/death cross, MACD cross and Bollinger bounce vs buy-and-hold. Earlier run (19 stocks, ~2 yrs): Bollinger most consistent, MACD roughly random, cross trailed hold in strong uptrends.
- **Short ideas tab**: scans a separate ~110-stock universe (`universe.json`, cache `universe_cache.json`), ranks top 5/10/15 by short score, flags risks (hard to borrow, not shortable, etc.), and has a "how long to short for X% gain / accept Y% loss" estimator. Buttons: Short this stock, Add to watchlist.
- **Trade tab**: live Last price label; Buy/Sell become "Buy to cover"/"Sell short" from holdings; take-profit/stop-loss can be entered as price, $ from price or % from price; limit/stop/trail prices auto-suggested from the stock's volatility; "Use suggested exits" button.
- **v0.17 Overview tab**: new top-level tab bar (Overview | Analysis) above the old tabs. Overview lists open positions (stocks and options, long and short) with P/L and a signal score from golden/death cross, MACD and Bollinger (+1 helps the position, -1 works against it), backtest results, and notes (expiry, break-even, earnings, big gain/loss). Buttons: Open chart, Trade..., Add to watchlist. Last-used top tab is remembered (`gui_settings.json` key `top`).

#### Explained to the user (they asked)
- Time in Force, market vs limit orders, short selling mechanics, cost of an unfilled order (nothing).
- Borrow fees: Alpaca's blog titles say borrow fees were eliminated for easy-to-borrow stocks; hard-to-borrow stocks carry variable fees via locates. Exact figures not verified, see alpaca.markets/support/short-selling-fees.

#### Testing status
Logic was tested with stubs and synthetic data only; Qt itself can't run in my environment. The user confirmed charts, options, strategies and the short/price features working through v0.16. v0.17 (Overview) is untested on the PC: check the tab shows, positions fill within ~30 s, detail text reads sensibly, buttons switch to the right tabs, theme switch looks right.

#### Not built
Multi-leg option strategies, exercising options, options in the watchlist score, MACD sub-panel. Python-version issue above is still unresolved.

#### To do next: watch program (added 2026-10-11, user request)
- Create a "watch" program for TradeBot GPU that runs in the background and sends the user a message with information from the app (for example position P/L, strategy signals changing, price alerts, earnings coming up).
- Not yet designed. Open questions to settle first: how the message is delivered (phone push, email, desktop notification), what should trigger it (schedule vs. events), and whether it runs inside the app or as a separate script. Must stay paper-only and read-only: no orders placed by the watcher.

---

## TradeBot: Restart menu (v0.18) and phone-alert watcher (watch.py) (2026-10-12, morning; follows a phone chat the night before)

Companion to the "TradeBot GPU: v0.08 to v0.17" section. Paper-only throughout. Full phone-chat notes: `2026-10-11_TradeBot-phone-alerts_handoff.md` (written before the real code was visible, so its template files are superseded by what is below).

### User goals (stated)
Not chasing a guaranteed-profit algorithm: wants an easy app that reduces risk, lets them learn as they go, and stays on paper trades while they improve formulas and strategies. Wants to keep adding ideas from their phone. Dropped idea: stock "mood" emoji (wasted effort).

### Built today (NOT yet run on the PC; tested only on made-up data in a sandbox)
- **TradeBot menu with Restart (v0.18)**: new "TradeBot" menu in `tradebot_gpu.py` with "Restart TradeBot" (Ctrl+Shift+R, asks yes/no first) and "Quit" (Ctrl+Q). The two run `.bat` files now set `TRADEBOT_LAUNCHER=bat` and loop: the app exits with code 3 and the bat starts it again. If started another way, it relaunches itself with `QProcess.startDetached`. It never touches orders. Backups: `TradeBot-GPU\backups\` (tradebot_gpu_backup_before_restart_menu_v0.17.py and both bats).
- **watch.py** (new, in TradeBot-GPU; reuses `analysis.py`, `tradebot.py`, `broker.Broker.snapshot()`; read-only, refuses non-`PA` accounts, never orders). Modes: scan (default), `--summary`, `--watchdog`, `--test-alert`, `--dry-run`, `--force`, `--selftest`.
  - Alerts on the phone through ntfy.sh: stock enters buy zone (score >= 75), a HELD stock drops to "avoid" (< 40), price >= 5% from previous close (once a day per stock), a position at your stop rule (stocks -7%, options -40%, from `risk.RULES`), watcher failures and a stale-scanner watchdog (urgent). Each alert includes the top 3 "why" reasons from `analysis.py`. First scan only sets a baseline (and sends one "watcher is running" message). Zone changes use a 2-point margin so scores near a line don't spam.
  - Scans only when Alpaca says the market is open. Fundamentals (yfinance) fetched at most once a day per stock and cached.
  - Files it creates in TradeBot-GPU: `watch_settings.json` (thresholds + private ntfy topic, created on first run), `watch_state.json`, `watch_log.csv` (every reading; feeds `review.py`), `watch_heartbeat.txt`, `watch_fund_cache.json`, `watch_log.txt` (errors).
  - Helpers: `notify.py` (ntfy, quiet hours 10pm-7am, only high/urgent pass), `risk.py` (rules + position sizing, not yet wired to any order), `review.py` (how buy/neutral/sell readings did 1/5/20 days later vs baseline), `Run_Watch.bat` (manual runs).
- Python: scheduled jobs should use `py -3.11` (has pandas, PySide6, alpaca-py, agent-reach). 3.15 also has the libraries. 3.14.8 has only pip and no venv uses it, so it is safe to uninstall. `myenv` and `PyCharmMiscProject\.venv` were built on Python 3.13.3, which `py -0` does not list: check `AppData\Local\Programs\Python` before removing anything else.

### Things to test
1. Start TradeBot GPU with Run_TradeBot_GPU.bat: title says 0.18 and a "TradeBot" menu sits left of Settings.
2. TradeBot > Restart TradeBot: pick No (nothing happens), then Yes (window closes and the app reopens by itself, same console window).
3. Try Ctrl+Shift+R, and the Safe .bat the same way.
4. In a command window in TradeBot-GPU: `py -3.11 watch.py --selftest` (fake data, sends nothing).
5. `Run_Watch.bat --test-alert --dry-run`, then without --dry-run: note the topic it prints, subscribe in the ntfy app, confirm the test message arrives.
6. `Run_Watch.bat --force` outside market hours: confirm "Scanned N stocks" and a "watcher is running" message; run again and confirm no repeats.
7. Check `watch_log.csv` is filling and `watch_log.txt` is absent or empty.

### Not done
- Task Scheduler jobs (every 15 min scan; one daily `--summary` ~3:15pm CT; hourly `--watchdog`), using `pyw -3.11` so no window flashes.
- Earnings-date warning, market-context tag (e.g. broad market above its 50-day average), confirm-first paper trades, weekly scorecard, trade journal, backtester hooks, strategy versions, equity curve vs index fund, habit badges.
- Thresholds (75 / 40 / 5% / -7%) are guesses; set them from real watch_log.csv data after a week or two.

### Addendum 2026-10-12 (later): TradeBot GPU v0.19, 12H / 24H ranges with 15-minute candles
- Two new range buttons at the left of the range row: **12H** (last 48 candles) and **24H** (last 96 candles), drawn from **15-minute candles**. "12 hours" means 12 hours of MARKET time: regular session only (9:30-16:00 ET), overnight and weekends skipped, so 24H is about 3.7 sessions. Hover shows the candle's time; header says "15-minute candles". Hourly candles already existed on 1M and 3M (header says "hourly candles" when loaded; log line "hourly candles loaded for N/N").
- Code: `core.py` (INTRADAY, M15_TTL, M15_DAYS, DataStore.maybe_fetch_m15 / _m15_worker / m15_frame, ChartModel.build uses the 15-minute frame when range is 12H/24H), `tradebot.py` (`fetch_bars(..., minutes=15)`), `tradebot_gpu.py` (range handling, "m15" / "m15_err" events, fetch on range switch and after each refresh while a 12H/24H range is selected; 15-minute data is refetched at most once a minute and kept in memory only).
- On these ranges: no 50/200-day averages or "Averages vs price" panel (not meaningful on 15-minute bars), RSI is a 15-minute RSI, Bollinger/MACD/cross overlays are not available (a note says so). The small-chart grid stays daily (uses 1M while 12H/24H is selected). If 15-minute data is missing the chart falls back to the last few daily candles with a note.
- Data is the free IEX feed, which is thin; some 15-minute slots may have no candle, so 48/96 candles can cover a bit more than 12/24 hours.
- Tested only on made-up data (the chart builder output for 1M, 3M, 6M, 1Y and Max is identical to v0.18; Qt itself was not run). Backups: `TradeBot-GPU\backups\core_backup_before_15min_v0.18.py`, `tradebot_backup_before_15min_v0.18.py`, `tradebot_gpu_backup_before_15min_v0.18.py`.
- Window-size warning seen at startup ("Unable to set geometry ... minimum size 941x1142" on the LG monitor, available height 1017): user said nothing is cut off, so it was left alone. Cause is the tallest tab setting the window's minimum height; a scroll area would fix it if it ever matters.
- Things to test: (1) title says 0.19; (2) buttons read 12H 24H 1M 3M 6M 1Y Max; (3) click 12H: "loading 15-minute candles..." then 48 candles, header "over 12H · 15-minute candles"; (4) 24H shows 96 candles; (5) hover shows times like 10:30 AM ET; (6) zoom and pan work; (7) turn on RSI and Candles; (8) switch to 6M and back, nothing else changed; (9) check tradebot_gpu_log.txt for "15-minute candles loaded for N/N" and any ERROR; (10) outside market hours the last session(s) are shown.

### Addendum 2026-10-12 (late morning): TradeBot GPU v0.21 plus watch.py upgrades
Tested only on made-up data in a sandbox (Qt could not be run there; the P/L bar geometry and journal read/write were tested as plain Python). Backups of everything changed are in `TradeBot-GPU\backups\` (names end `_before_journal_pnl_v0.19.py`, `watch_backup_before_earnings_weekly.py`).
- **Overview P/L chart (v0.21)**: new `PnlBars` widget in `qt_widgets.py` between the positions table and the detail text on the Overview tab. One bar per open position: gains go right in green, losses go left in red, with "+$x (+y%)" labels. Options are labelled like "DKNG 25C 11-20". If there are too many positions for the height, it shows the largest ones and says so in the corner. Updates whenever the Overview refreshes (about every 30 s) and follows the theme.
- **Trade journal (v0.20)**: after you confirm a paper order (stock, option) or Close position, a small box asks "Why are you making this buy of NVDA?" Optional; Cancel or empty still places the order. Entry is saved to `journal.csv` (time, kind, symbol, side, amount, type, limit, price at the time, score at the time, reason) only after Alpaca accepts the order. Close-all and cancels are not journaled. Code: `trade_qt.py` (`_journal_ask`, `_journal_write`, hooks in `review`, `review_option`, `close_selected`, `on_acted`).
- **watch.py additions**: (1) earnings: a heads-up alert 2 days before a stock reports (once per report; high priority if held), and "Earnings in N days" appended to buy / big-move / weakening alerts and the daily summary when within 7 days; dates come from `core.fetch_earnings` (Yahoo), looked up once a day per stock (`watch_earn_cache.json`). (2) market context: SPY vs its 50-day average appended to buy alerts, the first message and the daily summary, with a note that buy signals are less reliable below it, plus an alert when SPY crosses its 50-day. (3) `--weekly` scorecard: counts of alerts by kind (from the new `watch_alerts.csv`), paper equity and open positions, signal results from `watch_log.csv` via `review.py` (says "too early" under 30 readings), and this week's journal entries with the price move since; also written to `weekly_report.txt`. New settings in `watch_settings.json`: `earnings_warn_days`, `earnings_note_days`, `min_signal_samples`.
- **To do**: schedule the weekly scorecard (Fridays after the close), e.g. `schtasks /create /tn "TradeBot Weekly" /sc weekly /d FRI /st 15:30 /tr "pyw -3.11 \"C:\Users\cheye\Desktop\Claude Handoff\TradeBot-GPU\watch.py\" --weekly" /f`. Thresholds still guesses. Remaining ideas: confirm-first trades from the phone, strategy versions, equity curve vs index fund, habit badges, backtester.
- **Things to test**: (1) title says 0.21; (2) Overview tab shows the P/L bars under the table and they match the table; (3) place a tiny paper order: confirm it, a "Trade journal" box appears, type a reason, and a row appears in `journal.csv` after the order is accepted; (4) cancel the journal box and confirm the order still goes through; (5) `py -3.11 watch.py --selftest`; (6) `Run_Watch.bat --weekly --dry-run` (prints the scorecard); (7) check the next scheduled scan still updates `watch_heartbeat.txt` and `watch_log.txt` stays absent; (8) look for a new `watch_alerts.csv` and `watch_earn_cache.json`.

### Addendum 2026-10-12 (midday): TradeBot GPU v0.22, maximize and single-instance fixes
- **Not fully maximizing**: the startup warning "Unable to set geometry ... mintrack=(957,1181)" showed Windows was told the window can never be shorter than about 1181 px (the tallest tab's minimum), which is taller than the 1080 px LG monitor, so it could not fully maximize. Fix in `tradebot_gpu.py`: explicit `self.setMinimumSize(1000, 640)`. A tall tab is squeezed a little instead (it was already being squeezed to 1017 px before). 1.5 s after start the app logs the real minimum height of each page ("layout minimum heights: ...") in `tradebot_gpu_log.txt`, so the tallest tab can be trimmed properly later if anything looks cramped. Backup: `backups\tradebot_gpu_backup_before_maximize_single_instance_v0.21.py`.
- **Multiple copies**: new `single_instance()` uses a Windows named mutex (`Local\TradeBotGPU_single_instance`), released by Windows when the app ends or crashes, so no lock file can go stale. A second copy exits quietly (code 0, no pause in the .bat) and brings the open window to the front; if it cannot find it, it shows "already open". The Restart menu still works: the .bat path waits for the old process to exit; the non-.bat path sets `TRADEBOT_RESTARTING=1` and the new copy waits up to 15 s. Safe and normal launchers share the one lock. Copies started before v0.22 do not hold the lock, so close any old windows once.
- Tested only as logic (fake mutex table) in a sandbox; Qt/Windows not run there.
- Things to test: (1) close every open TradeBot GPU window, then start it: it should fill the whole monitor (check the bottom edge); (2) start it a second time while it is open: no second window, the first comes to the front; (3) minimise the first, start again: it is restored; (4) TradeBot menu > Restart still reopens exactly one window; (5) kill the app from Task Manager, then start again: no "already open" message; (6) check `tradebot_gpu_log.txt` for the "layout minimum heights" line and send it if any tab looks cramped.

### Addendum 2026-10-12 (late morning): own process names in Task Manager (bin\TradeBotGPU.exe, bin\TradeBotWatch.exe)
- Problem: every Python program shows as "Python" in Task Manager, so the app and the watcher's scans could not be told apart (user killed Python processes by hand; the scheduled scans survived, the 10:54 scan ran).
- Solution: `make_launchers.py` (run by `Setup_Launchers.bat` with `py -3.11`) builds `TradeBot-GPU\bin\`: `TradeBotGPU.exe` = copy of Python 3.11's python.exe, `TradeBotWatch.exe` = copy of pythonw.exe, plus python311.dll, python3.dll, vcruntime140*.dll and a `pyvenv.cfg` (home = the Python 3.11 folder, include-system-site-packages = true) so the copies use the real install's standard library and packages. Each copy's version information is rewritten through the Win32 resource API (BeginUpdateResource/UpdateResource) so FileDescription = "TradeBot GPU" / "TradeBot Watch", which is what Task Manager's Processes tab shows; the Details tab shows the new file names. Python's own icon and manifest are kept; nothing in the Python install changes. The script first checks that the Python running it has PySide6, pandas, alpaca, yfinance and psutil, then starts each copy once (`-c "import ..."`) to prove it works, then offers to (re)create the scheduled tasks: TradeBot Watch (15 min), TradeBot Summary (weekdays 15:15), TradeBot Weekly (Fri 15:30, new) on TradeBotWatch.exe; TradeBot Watchdog stays on `pyw -3.11` on purpose so it can still alert if the copies ever break. `bin\ABOUT.txt` explains the folder.
- `Run_TradeBot_GPU.bat`, `Run_TradeBot_GPU_Safe.bat`, `Run_Watch.bat` now use `bin\TradeBotGPU.exe` and fall back to `py -3.11` if bin is missing (deleting bin is always safe). `Install_Requirements.bat` now installs into Python 3.11 (was plain `python`, which is 3.15 on this PC). Backups of the old .bat files: `backups\*_backup_before_launchers.bat`. Note: the GUI had been running on Python 3.15 today (plain `python`); with the launchers it runs on 3.11, which has the same PySide6/pandas/alpaca versions and is what the watcher already used.
- Tested: `make_launchers.py --selftest` (version-block builder/parser, copying, pyvenv.cfg) on Linux only; the Windows-only parts (resource rewrite, start-up check, schtasks) have NOT been run yet. Re-run Setup_Launchers.bat after any Python update/reinstall.
- Possible later extra: give the copies their own icon (RT_ICON/RT_GROUP_ICON) so the taskbar and Task Manager show a TradeBot icon instead of Python's.
- Things to test: (1) close TradeBot GPU, double-click `Setup_Launchers.bat`, read the output: both copies should say "Task Manager will show ..." and "check ... ok"; answer Y to the scheduled-task question; (2) open the app with Run_TradeBot_GPU.bat and look at Task Manager: Processes tab shows "TradeBot GPU", Details tab "TradeBotGPU.exe"; (3) run `Run_Watch.bat --dry-run --force` and confirm it still scans; (4) after the next quarter hour, `watch_heartbeat.txt` updates (the scheduled task now runs TradeBotWatch.exe) and during a scan Task Manager shows "TradeBot Watch"; (5) Task Scheduler lists TradeBot Watch, Summary, Weekly, Watchdog; (6) if Windows Defender ever quarantines a copy, delete bin and the .bat files fall back to plain Python.

---

## Addendum - console window fix (2026-10-12)
- Cause: bin\TradeBotGPU.exe was a copy of python.exe (console program), so the app always had a command window behind it.
- Fix: it is now a copy of pythonw.exe (windowless). Run_TradeBot_GPU.bat / _Safe.bat launch it with `start` and close at once; Restart uses the app's own relaunch (QProcess, TRADEBOT_RESTARTING) instead of the bat loop.
- New Run_TradeBot_GPU_Debug.bat: console version (py -3.11) with the exit-code-3 restart loop, for seeing startup errors.
- Needs: close the app, run Setup_Launchers.bat again (rebuilds TradeBotGPU.exe). Backups in TradeBot-GPU\backups\*_before_windowless.*
- Pending: custom taskbar/exe icon (user request) - plan: make an .ico, set it via QApplication.setWindowIcon + AppUserModelID in tradebot_gpu.py, and write it into the exe's icon resources in make_launchers.py.

---

## Addendum - restart fix v0.23 and icon v0.24 (2026-10-12)
- v0.23: restart releases the single-instance lock (release_instance) before relaunching; relaunch result and "waiting" are logged in tradebot_gpu_log.txt. Cause of failed 2nd restart was not certain (lock held too long, or bat file replaced while running).
- v0.24: icon = glowing blue sphere with an orbiting ring carrying candlesticks (tradebot.ico + tradebot_icon.png in TradeBot-GPU; made with a Pillow script, not kept in the folder). tradebot_gpu.py sets the window icon and AppUserModelID "TradeBot.GPU.Paper" (own taskbar button). make_launchers.py set_icon() writes the icon into bin\*.exe (Windows only, untested until Setup_Launchers is run).
- Backups: *_before_restart_fix_v0.23.py, *_before_icon_v0.24.py, make_launchers_backup_before_icon.py.

---

## Addendum - icon redesign (2026-10-12)
- Icon v2 replaces the candlestick sphere (kept in TradeBot-GPU\backups\tradebot_icon_v1_candlestick.*): dark rounded square, Rook-style dot sphere (cyan to magenta by latitude), six thin tilted data orbits with glowing lights (colors from orbit-menu.html), and one larger orbit carrying two arrows (green = buy, red = sell) chasing each other.
- Regenerate with TradeBot-GPU\make_icon.py (needs pillow + numpy), then run Setup_Launchers.bat. Files: tradebot.ico, tradebot_icon.png. No code change; app is still v0.24.
- Ideas: tweak arrow colors/size, animate the in-app version later.
- Confirmed by user on the PC (2026-10-12): v0.23 restart fix, windowless launcher, and new icon all tested good.

---

## Addendum - Rook chat box v0.25 (2026-10-12)
- New chat box "Rook" bottom-left of TradeBot GPU (vertical splitter under the watchlist; size saved as gui_settings.json "left_split"). Typed chat only, no audio. Ctrl+K focuses it (TradeBot menu > Talk to Rook).
- Files: rook_chat.py (no Qt: settings, history, Claude + OpenAI-compatible/LM Studio calls, tool definitions, persona), rook_qt.py (RookChat widget + RookSettingsDialog), host methods theme/rook_snapshot/rook_tool/open_rook_settings in tradebot_gpu.py. Backup: backups\tradebot_gpu_backup_before_rook_chat_v0.25.py.
- Providers: "claude" (needs ANTHROPIC_API_KEY line in .env, user adds it; never printed/logged; model default claude-sonnet-5-5) or "local" (LM Studio at http://localhost:1234/v1, model blank = loaded model; user is downloading Qwen3-VL 8B Instruct for the GTX 1080 PC). Switch in Settings > Rook settings... (rook_settings.json).
- Rook gets a plain-text snapshot (watchlist scores/prices, positions, selected stock reasons, next earnings, risk.RULES, last phone alerts). Tools: add_to_watchlist, remove_from_watchlist (asks the user to confirm), open_chart, refresh_data. NO order tool, by design; persona says so.
- Chat history: rook_chat_history.json (last 40 turns, text only; ignore/delete to reset or use Clear).
- Tested here: backend with fake network (all pass), chat flow with a fake Qt, snapshot/tools with fake app. NOT tested: real Qt rendering, real Anthropic or LM Studio calls.
- Ideas: show-chart-screenshot to the VL model, Rook reading watch_log/weekly report, streaming replies, strategy/risk explanations, phone Rook later.

---

## Addendum - Rook v0.26 (2026-10-12)
- User confirmed Rook chat works with the local model (LM Studio, qwen/qwen3-vl-8b, GPU offload 36, server on localhost:1234).
- Problem seen: the small model invented "$342 over the monthly loss limit" and offered to open the Trade tab (no such tool). Fixes: snapshot now includes "Total unrealized P/L" and says realized monthly P/L is NOT tracked; persona forbids own arithmetic and offering actions without a tool; new tool open_trade_tab(ticker, side) only pre-fills the Trade tab (user reviews and confirms; no order is placed).
- Unrelated: user saw an Alpaca error "insufficient qty available for order (requested 100, available 0)" from the Trade tab, most likely shares already reserved by an open sell order. Not yet diagnosed (asked user to check open orders).
- Backups: *_before_rook_fix_v0.26.*

---

## Addendum - v0.27 (2026-10-12)
- Rook chat now starts empty every time the app starts (rook_settings.json "keep_history": false by default; set true to keep chats between restarts). Clear button still works. Backups: *_before_clear_on_start_v0.27.*

---

## Addendum - v0.28: font size, intraday time axis, range-for-Rook (2026-10-12)
- Settings > Font size: Larger (+2) Ctrl+=, Smaller (-2) Ctrl+-, Reset Ctrl+0; limits -4..+8; saved as gui_settings.json "font_delta". Implemented via qt_theme.FONT_DELTA/fs() (style sheet + inline label sizes), qt_widgets.set_font_delta (chart/grid text), MainWindow.change_font/apply_fonts (row heights too). Fixed-size buttons/tables in the Trade tab are not scaled and may look tight at +6 or more.
- Chart time axis (core.ChartModel.build, "time_mode"): when intraday bars (15-minute, or hourly) leave >=150 px per day, the date bar shows clock times (spacing auto: 15/30/60/120/240 min) with the day name on a second line, and the bottom margin grows to 40 px. Vertical lines: faint every 15 min, firmer on the hour, strongest at a new day (12H and 24H, and any zoomed-in view). Strength constants: 0.075 / 0.14 / 0.30 (core.py, search c_min).
- Range for Rook: hold Shift and drag across the chart; release to select (band + "Selected: N bars +x%"). A "Range for Rook" note with a Clear range button appears above Rook's input; double-click the chart, change stock or change range tab clears it. core.describe_window/window_text give Rook open/close/high/low (with times), % change, volume vs the visible chart, RSI. The snapshot also always has a "Chart on screen" line (current range tab, zoom included) and, if set, "USER-SELECTED RANGE". New Rook tool set_chart_range(range) switches the chart's range tab. Rook only gets numbers, not the picture (persona says so).
- Tested offline: chart build/axis/selection with fake 15-minute data (rendered to an image and looked at), snapshot/tools with fakes. NOT tested: real Qt drawing, mouse drag, font changes on screen.
- Backups: *_before_font_axis_range_v0.28.py

---

## Addendum - v0.29 tooltip fix (2026-10-12)
- Candle tooltip text overflowed its box: width was measured in the proportional font but the lines are drawn in monospace (Consolas). measure()/approx_measure() now take mono=True and the tooltip uses it (core.py tooltip, qt_widgets.measure). Backups *_before_tooltip_fix_v0.29.py.

---

## Addendum - v0.30 overlays on 15-minute candles (2026-10-12)
- User report: Bollinger bands did not come back when unchecked/rechecked. Cause: the saved range was 24H (15-minute candles) and overlays were deliberately disabled there (v0.18 note). The toggle itself was fine on daily/hourly (verified with fake data).
- Now Bollinger bands (20 candles, 2 sd) and MACD crosses work on 12H/24H: indicators are computed on ALL fetched 15-minute candles (store.m15_frame(sym) with n=None) and then cut to the view, so they are warmed up. Golden/death cross stays off on 15-minute candles (50/200-day based) with a note. Backups *_before_15min_overlays_v0.30.py.

---

## Addendum - v0.31 (2026-10-12)
- Bollinger bands drawn at 75% strength (core.BB_OPACITY = 0.75; set 1.0 for the old look). Backups *_before_bb_opacity_v0.31.py.

---

## Addendum v0.32 - Rook's sphere and voice (TradeBot-GPU)
- Rook's animated sphere (rook_orb.py math, RookSphere in rook_qt.py) replaces her name in the chat header: idle turn, faster spin while thinking, swells with her voice while speaking. Clicking it stops her talking.
- Spoken replies: "Voice: on/off" button next to Clear (saved in rook_settings.json), plus Rook settings > speak / voice / speed / run on GPU. No microphone or listening.
- Voice = Kokoro via rook_tts_worker.py run under Desktop\Rook\venv (Rook folder is read-only here); rook_speech.py cleans/splits text and talks to it; WAVs play with winsound. Failures show a red note and Rook stays text-only. Log: rook_tts_log.txt.
- MainWindow.closeEvent now calls self.rook.shutdown(). VERSION 0.32. Backups: backups\*_before_voice_v0.32.py.
- Tested with fake Qt + fake voice worker only; real Windows playback and the real Kokoro voice are untested.
- v0.32 follow-ups (same day): spoken-text cleanup (money, decimals, tickers->names, rook_pronunciations.json), rook_timing_log.txt, local-model guards (repeat penalty, repeat filter, 3-sentence rule, facts-only rules, actions only run if the user's message asked for them, fresh snapshot after actions, rule-based share size line), chart text now says "START/END of the period".
- Close zooms: <=6 trading days visible = 15-minute candles, <=15 days = 30-minute (resampled from 15-minute data fetched with the hourly data, 100 days, memory only), then hourly, then daily. Constants core.M15_MAX_DAYS / M30_MAX_DAYS. Axis has tick marks per candle interval and bold hour labels. Falls back to hourly if the data is missing.
- 15-minute candles are cached in m15_cache.pkl (loaded at startup; background top-up of the last 4 days; full re-download if older than 3 days or the file is bad).
- 12H/24H tabs now use 5-minute candles (core.INTRADAY_MIN), max zoom there = 47 candles (INTRADAY_MIN_VIEW); a zoom box top-right of the chart shows "Zoom xN · n of m candles" (yellow "max zoom" at the limit). The 5-minute data is also stored in m15_cache.pkl and its download starts at launch. "My option positions" shows a note when no option is held. Bollinger bands use real alpha colours (core.with_alpha). Tested by the user: 15-minute zoom, startup zoom OK.
- Still open: voice speed/model speed comparison via rook_timing_log.txt; weekly scorecard task; Alpaca "available 0" order error; tune alert thresholds after a week of watch_log.csv.
- "Now" button (right of the range tabs): jumps to the newest bars at the closest zoom of the current tab (ChartModel.jump_now).

---

## Handoff - end of session 2026-10-12 (TradeBot-GPU v0.32)
Paper account only. Never print keys. The user tests items and reports back. End updates with a numbered "Things to test" list. Back up to backups\ before editing.

### State: everything below is on the PC and was confirmed working by the user unless marked untested
- Rook chat (local Qwen3-VL 8B via LM Studio, or Claude API): animated sphere header, spoken replies (Kokoro via Rook\venv, files rook_orb.py / rook_speech.py / rook_tts_worker.py; Voice on/off button; settings dialog has voice, speed, GPU), spoken-text cleanup (money, decimals, tickers -> names, rook_pronunciations.json overrides, common caps words like AVOID read as words).
- Rook guards for the small local model: repeat penalty, repeated paragraph/sentence filter, 3-sentence limit unless asked for more, facts-only rules (no MACD/support/resistance/share counts invented), actions (open chart, range, refresh, trade tab, add/remove) only run if the user's latest message asked for them (rc.tool_allowed), fresh snapshot after actions, "Rule-based size" line in the snapshot, chart text says START/END of the period. rook_timing_log.txt logs model time and time to first sound (not yet analysed: user could not tell if local or Claude is faster; the model reply was ~20s with several actions before the guard).
- Chart: 12H/24H now 5-minute candles (INTRADAY_MIN), max zoom 47 candles there (INTRADAY_MIN_VIEW); zoom box top-right ("Zoom xN - n of m candles", yellow "max zoom"); "Now" button right of the range tabs (jumps to newest bars at closest zoom); close zoom on other tabs: <=6 trading days = 15-minute candles, <=15 days = 30-minute, then hourly, then daily (core.M15_MAX_DAYS / M30_MAX_DAYS); axis ticks per interval and bold hour labels; Bollinger bands use real alpha (core.with_alpha, BB_OPACITY 0.75); "My option positions" shows a note when none are held; 15/30-minute and 5-minute candles cached in m15_cache.pkl (startup load, background top-up of the last 4 days, 5-minute download starts at launch).
- Version 0.32; MainWindow.closeEvent calls self.rook.shutdown().

### Gotchas for the next session
- device_commit_files often reports "written" but the file on the PC is the OLD one for a few seconds, or the first commit does not land. After every commit wait ~8s and compare md5sum of the PC file with the staged file; commit again if they differ. (Seen on core.py, rook_qt.py, rook_chat.py, rook_speech.py.)
- Do not run device_commit_files in the same turn as a bash call that reads the file.
- Fake-Qt tests live in the old session scratchpad only (test_voice_fake.py, test_rook.py, t30b.py etc.); they need re-creating if wanted.
- Real Qt rendering, real Windows audio and real Alpaca data can only be checked by the user.

### Still open
- Diagnose the Alpaca "insufficient qty available (requested 100, available 0)" order error (probably shares reserved by an open sell order).
- Weekly scorecard scheduled task; tune alert thresholds after a week of watch_log.csv.
- Ideas not started: keyboard shortcut for "Now", 15-minute candles zoomed out / 5-minute only zoomed in on 12H/24H, phone-confirmed trades, strategy versions, equity curve vs index, habit badges, backtester hooks.
- Usage note: this chat used up the user's usage credits ($22.42 of $40 spent this month, balance -$0.01). Start new chats per feature; Rook on "Local model" costs no API credit.

---

<!-- source file: 2026-10-11_TradeBot-phone-alerts_handoff.md (merged here 2026-10-12; headings moved down one level) -->
## Handoff: TradeBot headless + phone alerts (2026-10-11)

### Decided
- TradeBot works better as a background task with phone alerts than a GUI that has to stay open.
- Split into: headless engine (no GUI imports), phone alerts via ntfy.sh, Qt GUI as optional viewer on the same engine.
- CLI-Anything (HKUDS) was looked at and judged a weak fit: Alpaca already has an API. A small hand-written CLI is the simpler route if an agent should drive the bot.
- Claude scheduled tasks are cloud-only and can't see the PC, so not suited to run the bot itself.
- Stay on the Alpaca paper account; any buy/sell command should be confirm-first with a position-size cap.

### Built (template v2: buy/sell zone alerts, big-move alerts, daily summary; untested against real code)
- engine.py: stub scan_watchlist() returning symbol/score/price. Replace with real scoring.
- notify.py: ntfy.sh alerts. Set a long random topic (env var TRADEBOT_NTFY_TOPIC).
- run_headless.py: one scan, writes latest_report.txt, alerts only when a score crosses BUY_THRESHOLD (80). Supports --dry-run.

### Not done
- Could not read the user's TradeBot or TradeBot-GPU folders (session was not linked to the PC).
- Real scoring not moved into engine.py.
- Task Scheduler job not created (every 15 min, weekdays, market hours, run whether logged on or not).
- Optional: Telegram /status and /report commands; confirm-first paper-trade command.

### Next step
Link a session to the PC, read TradeBot-GPU, move scoring/Alpaca code into engine.py, then set up the scheduled run.

### User ideas (added later in session)
- Alerts wanted: score crossing buy threshold, big price move, sell signal; daily summary on phone. Check frequency set in Task Scheduler (e.g. every 15 min).
- Implemented as BUY_THRESHOLD=80, SELL_THRESHOLD=30, MOVE_PCT=5.0 in run_headless.py (all tweakable). Daily summary via `--summary`, second scheduled task (e.g. weekdays ~4:15pm CT).
- User will keep sending ideas from phone; user does NOT want any trading right now.

### Goal (user, stated)
Not chasing a guaranteed-profit algorithm. Wants an easy-to-use app that reduces risk, lets them learn as they go, and stays on paper trades while they improve formulas/strategies.

### Added: logging + review
- run_headless.py now appends every scan to score_log.csv (time, symbol, score, zone, price).
- review.py compares price change after buy/neutral/sell readings (1, 5, 20 days) against a baseline of all readings. Tested on synthetic data only.
- Thresholds (80/30/5%) are guesses: set them from real logged score ranges after a week or two of data.
- Possible next: "why" line on alerts (which score components drove it), backtest on Alpaca history, risk rules (max per trade, stop-loss, monthly loss limit) before any paper-trade automation.

### Accepted feature list (user approved all except #14 mood emoji, which is dropped as wasted effort)
Safety: 1 risk rules file [BUILT: risk.py] | 2 data/error watchdog [BUILT: --watchdog + heartbeat + failure alert] | 3 confirm-first paper trades [todo] | 4 weekly signal scorecard [todo, extend review.py]
Learning: 5 "why" line on alerts [needs real scoring code] | 6 backtester on Alpaca history [todo, needs desk session] | 7 numbered strategy versions [todo] | 8 trade journal [todo] | 9 position sizing helper [BUILT: risk.position_size]
Extras: 10 market-context tag (e.g. market above 50-day avg) [todo] | 11 earnings calendar warning [todo] | 12 quiet hours [BUILT in notify.py, 10pm-7am, high/urgent bypass; add work-meeting windows] | 13 equity curve vs index fund [todo]
Fun: 15 habit badges (e.g. followed own stop-loss N times) [todo]
Suggested first set: 1, 2, 5, 6.

### Built this round
- risk.py: RULES (max $/trade 500, max positions 5, stop 7%, monthly loss limit 300, risk/trade $25), position_size(), check_order(). Values are placeholders.
- notify.py: quiet hours.
- run_headless.py: --watchdog (run hourly; alerts if no good scan in 45 min, weekdays 9-4), failure alerts, heartbeat.txt.

---

## Fix: "bracket orders must be entry orders" (v0.33, 2026-10-14)
- Cause: selling shares you already hold (or buying back a short) with take-profit/stop-loss filled in was sent to Alpaca as a bracket order. Alpaca only allows brackets on orders that OPEN a position.
- Fix (trade_qt.py review + broker.py): when the order closes something held, exits are sent on their own: take profit + stop loss together as one linked OCO pair (sell/buy limit at TP and stop at SL, whichever fires first cancels the other); only one of them becomes a plain Limit or Stop order. The confirmation box says "EXIT ... two linked orders ... nothing is bought or sold right now". The typed order type is overridden in that case.
- Also fixed: take-profit/stop-loss direction for exits was reversed (a sell of held shares was treated like a short, wanting TP below price). Exits now follow the position: long = TP above / SL below. Suggested exits and "$/% from price" use the same rule. Buying more than the short you hold is now blocked with a message.
- Untested against live Alpaca (the OCO request shape follows Alpaca's docs). First real test: hold a few shares, Sell with a TP above and SL below the price, confirm, then check the Orders table shows both legs. If Alpaca rejects it, the red error text will say why.
- Heads-up: the TradeBot-GPU folder on the PC had moved on to v0.32 (watch program, journal, etc., from another session) and the chat's scratch copy was stale; this fix was applied on top of the PC's current files, not the scratch copy. Always stage the device files first.

## Fix: order ticket squished on 1080p (v0.34, 2026-10-14)
- On a shorter window the Trade tab's order ticket was squeezed to fit: fields clipped ("Dav", "Market" cut off) and the suggested-exits text overlapped. trade_qt.py now puts the ticket in a scroll area (fixed 370 px wide, scrolls vertically when the window is short), gives every field a 28 px minimum height and trims spacing slightly.
- Not visually verified (Qt can't run in the chat's environment). If corners or background around the ticket look wrong, the cause is the scroll area's background (card.setAutoFillBackground(False) / transparent QScrollArea style in `TradePanel.__init__`).

## Short ideas: double-click opens the chart (v0.35, 2026-10-14)
- Double-clicking a row in the Short ideas table opens that stock's chart on the Analysis > Chart tab (`short_open_chart` in tradebot_gpu.py). If the stock is not on the watchlist it is added first (the chart needs its prices) and a status message says so; if the watchlist is full (20) it says to delete one.

## Watchlist no longer capped at 20 (v0.36, 2026-10-14)
- The watchlist hit a fixed cap of 20 (`MAX_TICKERS` in core.py) and was full, so adds/double-click-opens were refused. The cap is now 200 as a safety ceiling only. Costs of a big list: longer refresh (company financials are fetched once per new stock, then cached 6 h), bigger `m15_cache.pkl`. The chart grid is still limited to 9 (`MAX_GRID`). The list scrolls; the left column's vertical splitter (between the watchlist and the Claude chat) resizes it.

## Watchlist: no limit, box resizes itself (v0.37, 2026-10-14; replaces the v0.36 ceiling)
- All watchlist size checks are gone (add button, double-click from Short ideas, Rook's add_to_watchlist, load from watchlist.json). `MAX_TICKERS = 200` is still defined in core.py but no longer used anywhere in tradebot_gpu.py; safe to delete.
- New `_fit_list()` in tradebot_gpu.py (called from `rebuild_list`): when the NUMBER of stocks changes, the watchlist box in the left column grows or shrinks to fit the rows (min 200 px, always leaves 170 px for the Rook chat below) and saves the split. It does nothing at startup or on plain refreshes, so a split the user drags by hand is kept until the stock count changes. Chart grid is still limited to 9 (`MAX_GRID`).
- Not verified visually (Qt can't run in the chat environment); the sizing maths was tested with a fake splitter.
