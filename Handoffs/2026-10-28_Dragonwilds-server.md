# RuneScape: Dragonwilds dedicated server (DESKTOP-2)

Self-hosted RuneScape: Dragonwilds dedicated server on DESKTOP-2 (the 2nd PC), for friends including PS5 players. Notes only; no code lives in the repo. Steam app ID for the server tool is 4019830; the client is 1374490.

## 2026-10-28 (main PC chat, server runs on DESKTOP-2) - server not showing in the browser: solved

Asked: where is the dedicated server config, can a PS5 join a modded server, which ports it uses, a .bat to launch with a console, then why the server would not appear in the in-game browser or accept the PS5 invite code.

### Resolved
- Cause: the game truncates names to 16 characters when it publishes the session. `ServerName` "FF Dragonwilds PC" shows as `FF Dragonwilds P`, and the world name "Forsaken Dragonwilds" shows as `Forsaken Dragonw`. The browser search matches the truncated text, so searching the full names found nothing.
- Fix: in Worlds > Public, search `Forsaken Dragonw`. Joined from PC, and the PS5 found it in the server browser too. The user considers it resolved.
- Optional cleanup (not done): set `ServerName` to 16 characters or fewer so the full name is searchable. Leave `DefaultWorldName` alone, because changing it can make the server create a new world instead of loading the save.

### Setup facts worth keeping
- Config file: `<server install>\RSDragonwilds\Saved\Config\WindowsServer\DedicatedServer.ini`. Stop the server before editing; changes made while it runs are lost. Keys in use: OwnerId, ServerGuid (generated, leave alone), ServerName, WorldPassword, AdminPassword, DefaultWorldName, PlatformPolicy=Crossplay.
- Install is the Steam Tool, under `C:\Program Files (x86)\Steam\steamapps\common\RuneScape Dragonwilds Dedicated Server`. Saves are under `RSDragonwilds\Saved\` (SaveGames, SaveCharacters).
- The real server exe is `RSDragonwildsServer.exe`. Launcher .bat (`start-dragonwilds-server.bat`, in the install folder): `cd /d "%~dp0"`, then `RSDragonwildsServer.exe -log -Port=7777`, then `pause`. `-log` opens the console; the log file is `RSDragonwilds\Saved\Logs\RSDragonwilds.log`.
- Ports: UDP 7777 is the game port. The log also shows a "world settings beacon" listening on UDP 8888. Vilo router app: 7777 UDP is forwarded to DESKTOP-2 (192.168.58.106, DHCP reservation set). 8888 is not forwarded and the user did not need it for the PS5/PC browser join.
- Earlier mistake found along the way: 7777 had been forwarded to the main PC instead of DESKTOP-2. A router can send an external port to only one device.
- Vilo: a second rule sends external 27015 to another PC (192.168.58.105, internal 27017) for a different game. 27015 turned out not to matter for Dragonwilds; leave that rule alone.
- Server and client builds must match (both were `hotfix-CL-254097` at the time). A mismatch hides the server from the browser with no error. Restart the server after every patch.
- Invite code is regenerated every server start; read the current one from the pause menu while connected or from the startup log (`JoinCode`).
- Hairpin NAT: direct connect by public IP:port worked from inside the home network, so it was not the issue.
- Mods: client-side mods are not supported on console; only server-side mods work for PS5 players.
- SteamCMD update command (no `validate`, one guide says it can wipe the config): `steamcmd.exe +force_install_dir "<server folder>" +login anonymous +app_update 4019830 +quit`. It threw "Missing configuration" once; not needed, since the client and server builds already matched. Back up `DedicatedServer.ini` and `Saved\` before updating.

### Not checked
- A friend joining from outside the home network was not tested separately; the user is treating the issue as resolved.
