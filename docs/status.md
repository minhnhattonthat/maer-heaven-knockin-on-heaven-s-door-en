# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** Step 0 (repo setup) done -> next is phase 1 (research and recon). Last build: none yet (2026-10-31).
- **Done:** template files; `tools/skill.py`; MesenCE 2.2.1 + GBA BIOS in `tools/mesen/`; `rom.sha1` pinned (5ed178bf..., BM9J, 16 MiB); smoke on the original ROM passes (`work/qa/smoke-orig`: Konami logo -> title -> Start reaches the main menu "ストーリーモード / ARM 対戦モード / 対戦モード / ..."); Lua probe logs (`tools/lua/probe_log.lua`); plugin guard hook blocks `sed -i`; pre-commit (`tools/hooks/`, core.hooksPath) rejects a failing test; `tools/check.py` + `tests/`.
- **Next:** phase 1: earlier patches / docs search, text encoding (likely SJIS, check), pointer tables, compression (LZ77 BIOS calls?), free space inside the full 16 MiB ROM, graphics-text survey (title logo, main menu items are tile graphics). Record in `docs/re/`.
- **Open bugs:** none.
- **Waiting on the user:** GUI keyboard input in `tools/mesen/Mesen.exe` not checked by a human (headless only; Mesen fills default key mappings on first GUI start, `ConfigUpgrade: 1`). Non-blocking.
