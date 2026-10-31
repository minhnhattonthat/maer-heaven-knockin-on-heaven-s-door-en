# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 4 (extract) done -> next is phase 5 (engine spike + marker build + width gate). Last build:
  `build/maer_en.gba` = original, sha1 5ed178bf... (identity, 2026-11-01).
- **Done:** Step 0, phase 1 (recon, `docs/re/`). Phase 4 (2026-11-01):
  - `tools/extract.py` -> `script/spc/<NAME>.json` (170 scripts, 5 563 lines, 3 199 unique), `script/code.json`
    (136 string-block strings + pointer refs), `script/records.json` (917 ARM/item name+desc fields); codec
    `tools/text.py` (`{C0F04}` colour codes, `♥`/`Ä` user glyphs); format in `docs/re/text.md` §Script files;
  - `tests/test_extract.py`: roundtrip of every string, coverage of scripts / string block / record fields,
    `script/` in sync with the ROM, re-extract keeps `en`;
  - recon fixes: ARM desc field is 0x22 bytes (not 0x30); item table 0x1BE7E0 (0x50-byte records); no JP text
    anywhere else (strict sweep of code + non-script archive files).
  Phase 3:
  - `tools/build.py`: unpack MAR.NFP -> `scrp.rebuild` every script -> repack -> ROM; no edits = byte-identical
    (`tests/test_build.py`); `build(rom, edits={SPC: {pos: bytes}})` is the insert hook for phase 4+;
  - `scrp.rebuild` relocates jumps/switches/0x22 string addresses/FUNC fixups (lengthen-all-strings roundtrip test);
    SCRP files end in `TERM`, NVAR size counts its header (`docs/re/script.md`);
  - overflow: archive jumps the fixed block 0xF28406-0xF2B447 into free space after an `.SPC` (implicit file size =
    next offset, `docs/re/nfp.md` §Rebuild); `build.py --recompress` test ROM: smoke ok, 73/73 warps same screens.
  Phase 2:
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
- **Next:** phase 5: read the text renderer (ARM 0x08000800-0x08000D40 + MswStr) to decide font/VWF (8x8 fixed
  font, 26-cell box, single-byte ASCII support unknown); marker build `[id]` per line via `build(edits=)` for
  scripts, repointing for `code.json` (refs; the 0x13D884 subref needs its own string) and in-place fields for
  records (max 33 bytes); measure every box variant (dialogue, menus, ARM desc, shop, link messages). Our LZ77 is
  greedy (+2% vs original): an optimal-parse compressor would cut spill if space gets tight (723 KiB free).
- **Open questions for later phases:** single-byte ASCII support in the text renderer (ARM blitter 0x08000800-0x08000D40);
  exact meaning of `C`/`T` codes; whether any `0x29` push carries a code offset (append-strings strategy avoids it);
  EWRAM script buffer size; ÄRM交換 mode shows nothing without a link partner; screens not yet in the scene list:
  link-cable messages past PARTY SELECT, password entry, save prompt (`docs/re/debug.md` §Not reached).
- **Open bugs:** none.
- **Waiting on the user:** GUI keyboard input in `tools/mesen/Mesen.exe` not checked by a human (headless only). Non-blocking.
