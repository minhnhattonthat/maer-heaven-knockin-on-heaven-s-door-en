# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 5 (engine + marker + width gate) nearly done; one item left (code-string label budgets, see Next).
  Last builds (2026-11-01): `build/marker.gba` (`build.py --marker`), `build/widthtest.gba` (`tools/widthtest.py`);
  `build/maer_en.gba` = original (identity).
- **Done:** Step 0, phase 1 (recon, `docs/re/`). Phase 5 (2026-11-01, `docs/re/vwf.md`):
  - renderer read: one glyph blitter at any pixel x (0x08011688), 5 font users (dialogue, 2 list renderers,
    2 centred labels); single byte b -> glyph b+0x1E0, so ASCII goes into those font slots;
  - `tools/engine.py` (keystone, hooks at 0xFE4000): VWF in dialogue, list windows and centred labels;
    English font `fonts/vwf8.txt` (drawn, MIT); C/T codes need 4 hex digits after them; `text.encode_en`;
  - **script rule found**: CODE size must stay 2 mod 4 (VM stack-top write; else heap header smashed, black
    screen); `scrp.rebuild` NUL-pads the last changed string (assert);
  - marker build: every script line `[n]`, code strings `[cN]` (repointed to 0xFE8000+), records `[rN]` in place;
    ids `build/marker_ids.tsv`; 73/73 warps ok, every font-drawn text shows ids (`work/qa/scenes/sheet*.png`);
    `jp_left --gba-ptrs` on it: 3 noise hits only (CHR.NCD tile word -> 0x088880, two data words);
  - width gate `script/windows.json`: dialogue 192 px x 3 lines (label + 2; narration 3) measured; ÄRM name
    112 px and desc 150 px measured (minimums; 33-byte field limit too); torture line renders all ASCII;
  - CH_ESC.SPC stays Japanese (debug chapter select; warp.lua jumps to fixed offsets in it): `build.KEEP_SCRIPTS`;
  - probes: `tools/lua/boxshot.lua` (shot per finished dialogue box), `heaplog.lua`, `wwatch.lua`.
  Phase 4 (2026-11-01):
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
- **Next:** finish phase 5: measure the code-string label fields (`windows.json` `code_labels`: element/stat/area
  labels, ばんごう/コスト/..., digit strings ０-９, which compose numbers: decide ASCII digits) with a `--qa`-style
  override for code.json in `widthtest.py`; try ÄRM name > 112 / desc > 150 (status box); then give every
  code.json entry its window. Then phase 6 (translate): add the text lint (width per `windows.json`, codes,
  `[CcTt][0-9A-Fa-f]{4}` inside English text = accidental control code). Our LZ77 is greedy (+2%): an
  optimal-parse compressor would cut spill if space gets tight (723 KiB free; marker build fits).
- **Open questions for later phases:**
  exact meaning of `C`/`T` codes; whether any `0x29` push carries a code offset (lengthening every OPEN.SPC string
  works, so none there); ASCII format strings in the string block (`T0000 C0F04 %s`) now draw their spaces (3 px);
  EWRAM script buffer size; ÄRM交換 mode shows nothing without a link partner; screens not yet in the scene list:
  link-cable messages past PARTY SELECT, password entry, save prompt (`docs/re/debug.md` §Not reached).
- **Open bugs:** none.
- **Waiting on the user:** GUI keyboard input in `tools/mesen/Mesen.exe` not checked by a human (headless only). Non-blocking.
