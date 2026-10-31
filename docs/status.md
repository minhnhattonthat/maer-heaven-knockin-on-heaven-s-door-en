# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 2 (debug tool) done -> next is phase 3 (identity build). Last build: none yet (2026-11-01).
- **Done:** Step 0, phase 1 (recon, `docs/re/`). Phase 2:
  - the game's leftover debug room (DBG_ESC.SPC) and debug chapter select (CH_ESC.SPC, 40 questions) drive the warp:
    `tools/debug/warp.lua` redirects the new-game script lookup, then patches CH_ESC's first jump in RAM
    (`docs/re/debug.md`);
  - `tools/debug/scenes.lua`: every story stage, ending, staff roll + last page + CLEAR PASSWORD, title/copyright/
    mode list (also with the locked modes unlocked), versus PARTY SELECT, dungeon-mode menu, all 5 dungeon gates
    (BF1 banner), field battle / ÄRM SELECT / WIN / GAME OVER, main menu + deck/item/status/ÄRM list, world map
    AREA SELECT, all 7 shops, engraver, portrait viewer, full items, all party;
  - `tools/debug/regen.py`: every scene from a cold boot -> `work/states/<scene>.mss` + proof shot (sheet in
    `work/qa/scenes/`); last run 73/73 ok, proof sheets read (ÄRM交換 shows no lit sprite; `pelica_free` stops on the next debug
    question, answer いいえ as the `menu` route does);
  - god mode (`--var GOD=1`), flag/var setters, battle-HP and title-mode-unlock addresses: `docs/re/debug.md`;
  - `tools/scrp.py dis NAME.SPC` now names native calls; tests `tests/test_debug.py`.
- **Next:** phase 3 identity build: rebuild MAR.NFP (directory + files, LZ77 re-pack or stored copy) and the
  scripts with no edits; the rebuilt ROM must be byte-identical, as a test. Then `tools/build.py`.
- **Open questions for later phases:** single-byte ASCII support in the text renderer (ARM blitter 0x08000800-0x08000D40);
  exact meaning of `C`/`T` codes; whether any `0x29` push carries a code offset (append-strings strategy avoids it);
  EWRAM script buffer size; ÄRM交換 mode shows nothing without a link partner; screens not yet in the scene list:
  link-cable messages past PARTY SELECT, password entry, save prompt (`docs/re/debug.md` §Not reached).
- **Open bugs:** none.
- **Waiting on the user:** GUI keyboard input in `tools/mesen/Mesen.exe` not checked by a human (headless only). Non-blocking.
