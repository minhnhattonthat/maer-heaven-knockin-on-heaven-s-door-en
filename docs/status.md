# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 9 in progress (story pass, then release). Phase 8 closed 2026-11-01: visual QA 135/135 ok; graphics
  rows not reachable from a cold boot are preview-checked only (`docs/qa-gfx.md`). `build/maer_en.gba` = full English build (every script line, code string and record; 73/73 warps ok).
- **Phase 9 (2026-11-01): story pass.** `tools/chapters.py` -> `work/qa/story/chapters/ch00-ch11.txt` (12 chapters
  from `docs/synopsis.md` headings); `qa_gate.py init work/qa/story/manifest.tsv ...`; one `reviewer` agent per
  chapter (`docs/story-reviewer-brief.md`), verdicts `work/qa/story/verdicts/<ch>.tsv`, Minors -> `docs/polish.md`.
  Other builds: `build/marker.gba` (`build.py --marker`), `build/widthtest.gba` (`tools/widthtest.py`).
- **Phase 8 in progress (2026-11-01): graphics text.** `tools/gfxtext.py` letters NCD sprite frames from
  `gfx/<BANK>.tsv` (`frames<TAB>English<TAB>options`; options in its docstring; `check`, `preview`, `colors`;
  build applies it to SYSTEM.NCD/EFFECT.NCD). Every lettered frame is relaid onto fresh sprites: 32-wide objects
  only (16/8-wide ones showed 8-16 px off in game), one run of consecutive tiles (free runs left by other relaid
  frames first, else appended), OAM tail tile count is **big-endian** (byte 19; LE = nothing loads). Growth limit:
  SYSTEM.NCD must end before the fixed block 0xF28406 (~90 KB slack minus script growth; now +39 KB): past it the
  build fails "archive past 0xFE0000". Fonts: Pixelify Sans Medium 13/11 (OFL) + vwf8 (small, Ä added).
  Done in SYSTEM.tsv and seen in game: main menu, mode banners, area names, gate banners, tags, command windows,
  smith menu, prompts, button hints, link messages (link/prompts/smith not seen in game yet), staff roll
  1698-1781 (D15; `wl=` grows right-aligned frames left, right edge = old ink edge), ÄRM type balls 0624-0635
  (`bgrow=`), big Story/Dungeon Mode banners (`font=huge`), mode option bars 1893-1906 (`bgrep=`, `grad=`);
  EFFECT.tsv: Sealed 0386-0389, Stats wipe 0402-0406. BG screens via `tools/bgtext.py` + `gfx/BG.tsv` (map cells
  re-tiled, KCG re-compressed; per-cell palette bank kept unless `pal=`): title logo redrawn (D16), copyright,
  smith ÄRM grades, OWNED. Space: SYSTEM.NCD grew +130 KB; `nfp.pack` now moves `MAP42_A.KMP` past the gap when
  needed (verified in game, docs/re/nfp.md). Visual QA: `tools/tour.py` (EN -> `work/qa/tour`, JP baseline
  `tools/tour.py <jp rom> --out work/qa/tour_jp`), `qa_gate.py init/todo`, verdicts by `tools/vqa_codex.py`
  (codex exec; its quota ran out until 2026-11-05, so round 1-2 used the `visual-qa` agents; verdict files
  `work/qa/verdicts/`, round 1 kept as `r1_*.tsv`). Round 1 fixes: **OAM x/y are object centres** (gfxtext read
  them as top-left: mixed-size frames were mis-composed; shop/yes-no/smith windows, Owned, Power left, hints, link
  messages, tags, mode bars re-tuned on the true layout; `bgrep` + `bgfrom` takes bar columns from another frame),
  Pixelify 11 px B/E/F replaced by plain 5x7 shapes (`gfxtext.OVERRIDE`), SPEC tag in the small font, text
  reading as a code across a colour code ("Ice{C0F04}" = "ceC0F": `{p1}` before the code, lint checks across
  codes), one-word last lines (`lint.wrap` moves a word down; `batches.py rewrap` re-wrapped 212 boxes).
  jp_left: 1 known noise hit. Round 2 (126 sheets) + round 3 (20): 0 issues; **`qa_gate.py check` passes
  (135/135)**; smoke ok; regen 73/73. **Left (phase 8 done-when):** graphics-text rows not yet in a cold-boot shot,
  listed in `docs/qa-gfx.md` (area names: trigger not found; smith with materials; input prompts: need a save;
  Sealed/Stats battle effects; other name tags; link messages: no partner). New scenes `mode_story`, `items_cmd`.
  Next: a `pre` step in warp.lua to run FULL_ITM before the engraver (smith 1583/1685 + recipe prompt), find the
  area-card and Sealed/Stats triggers (scripts: grep the SPCs for the card/effect calls), then phase 9.
  Polish: Pixelify 'e'/'G' read close to 'o'/'8' with outline+bold.
- **Phase 6 review fixes (2026-11-01, `.harness/reviews/...-phase6.md`):** Bellini's register (no dropped g's,
  polite + "nonn") in HI_M24 / L24_0_0 / CH_M24_A; `batches.check_unit` now matches glossary terms as whole words
  (s/es plural; any trailing letters only when the JP stretches the name: ギンタ～ン -> Gintaaan), record name fields
  equal to a glossary name must be exactly it, honorifics checked per name (どの/殿 -> -dono added; an English
  honorific the JP lacks fails); `lint.char_errors` rejects `%dth`-style suffixes and a/an before `%s`;
  negative tests in `tests/test_batches.py`. Synopsis: C0F04 is the white colour code, not a variable.
- **Phase 7 (2026-11-01):** every ROM write goes through `build.put` (log: offset, replaced bytes, new bytes,
  writer; `engine.apply(rom, log)` too); `build.make()` = the English ROM from lines + tables. `tests/test_romdiff.py`
  builds it in memory: `romdiff.check` with the log (no overlaps / overwrites / unlogged changes), every write inside
  the allowed spans (archive 0x1C0920-0xF28406, spill 0xF2B450-0xFE0000, engine 0xFE4000-0xFE8000, strings
  0xFE8000-0xFFF000, hook sites, sprintf formats, code.json refs, record fields), every record/code entry written
  and each repointed ref landing on its English, no Thumb branch within 4 KB landing inside a hook. `romdiff.check`
  now takes half-open ranges (an offset set of a 14 MiB archive needs GBs). Lint: non-empty jp with empty en
  fails (except CH_ESC, `keep` windows, fullwidth-blank fields). `jp_left --gba-ptrs` on the English build: 2 noise
  hits (0x3FA870 tile word -> 0x088880, whose real ref 0x1B0910 is repointed; 0x1ABF60 data word -> odd address in
  the rebuilt archive). In game: shop price/buy/sell ("200 P, please.", "Armor Stone CL1: / Bought!", "50 P is my
  offer.", "Knife Stone: / Sold!", "Not enough Pewter.", "Take it from where?"), WIN "Lightning Stone CL2
  obtained!!", stat-up "HP went up by  0 points!" (spacing -> `docs/polish.md`) all fit. Money cheat
  `tools/debug/cheat.lua` (`docs/re/debug.md`).
- **Phase 6 (2026-11-01):** tools `tools/batches.py` (split/check/merge/fit/labels/pairs; a unit = one message box,
  deduplicated; English auto-wrapped onto the box's lines, ' / ' forces a break; narration keeps its middle line and
  fullwidth-space centring), `tools/lint.py` (run by `check.py`: chars, widths, colour codes per box, code-string
  windows, record limits); extract also emits the 1 328 empty MswStr lines (spare lines; verified in-game,
  `work/qa/p6_spare/box_001402.png`); briefs `docs/translator-brief.md`, `docs/reviewer-brief.md`,
  `docs/story-reviewer-brief.md`; `docs/synopsis.md`, `docs/style-reference.md`, `glossary.md` (593 rows +
  wave-1 decisions; capitalised rows enforced by the batch check; honorific check only on Characters names);
  speaker labels filled (`batches.py labels`); 2 composed item boxes in DITEMCOM set by hand. 21 batches
  (b001-b015 script, b016 code strings, b017-b021 records) all check OK and merged; batch files live in `work/tl/`
  (gitignored; the English is in `script/`). Review: 6 reviewers, every batch read; Critical 0; Important fixed
  (Papa Rock Dor- joke, Bellini register, Talos 'Arms', Ed second-time line, Bellini Miss pun, shop imperative,
  Marl hint, WIN banner "P gained!!" / "%s obtained!!", きっと, 木 = Leaf, Halloween コゾウ = boy) and re-read by the
  controller; Minors in `docs/polish.md` (phase 9). Status element column widened (pad_to 26 -> 28,
  `work/qa/p6_status2`): "Water" fits, 雷 = "Bolt" (Thunder 35 px can't), no abbreviations left. パワーストーン ->
  "Powerstone" so Thunder CL names fit 112 px.
- **Done:** Step 0, phase 1 (recon, `docs/re/`). Phase 5 (2026-11-01, `docs/re/vwf.md`):
  - code strings (`script/windows.json` 'code'): every code.json id sits in one window (test); renderer per string
    from `tools/lua/drawlog.lua` + `tools/debug/drawmap.py` (`work/qa/drawmap/map.tsv`); measured with
    `widthtest --code-test`: status labels 38 px (+pads to 40), EXP header 104, elements 24 (+pads to 26),
    names 40, ÄRM class 84 + element 66, area names 124, GET!! 172, help/shop/save messages 192 (dialogue path;
    price-prefixed ones 144); fullwidth digits/slash/blanks stay Japanese (`keep`: copied 2 bytes per digit);
    status rows are 25-byte buffers (`bytes`);
  - engine additions: pad bytes 0x01-0x1F (`{pN}`, blank, N px in lists; build pads `pad_to` labels); ASCII in
    list windows skips the window's 1-px spacing; `pxlen` hook replaces strlen at 10 byte-count centring /
    right-align sites (names, area names); the dialogue fetch skips the space after `T0000` (menu help lost 3 px);
    17 ASCII sprintf formats lose the space after `C0F04` (`engine.FORMATS`);
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
- **Next:** phase 9: story-pass verdict per chapter (fix Critical/Important, regenerate, re-review),
  `docs/polish.md` ticked, release script, jp_left, debug tool off, patch verified. Optional: graphics rows still
  without a cold-boot shot (`docs/qa-gfx.md`; a `pre` FULL_ITM step in warp.lua would reach the engraver messages). Still unchecked in
  game: link-cable messages (no partner), sort headers (40 px guess). Speaker label "[---]" in the gate_* scene:
  check its JP. Our LZ77 is greedy (+2%): an optimal-parse compressor would cut spill if space gets tight.
- **Open questions for later phases:**
  exact meaning of `C`/`T` codes; whether any `0x29` push carries a code offset (lengthening every OPEN.SPC string
  works, so none there); EWRAM script buffer size; ÄRM交換 mode shows nothing without a link partner; screens not
  yet in the scene list: link-cable messages past PARTY SELECT, password entry, save prompt, ÄRM sort keys
  (`sort_headers`, guessed 40 px), the 'choose a character' label (`docs/re/debug.md` §Not reached). The
  `pxlen` rounding can leave right-aligned names up to 7 px short of the edge. Status-screen corner name, shop
  かう/うる menus etc. are graphics (`docs/re/graphics.md`), phase 8.
- **Open bugs:** none.
- **Waiting on the user:** D13 ÄRM type ball abbreviations (AT/DF/A+D/HEAL/SPEC) chosen on defaults; owner may
  override (docs/decisions.md). Non-blocking. GUI keyboard input in `tools/mesen/Mesen.exe` not checked by a human (headless only). Non-blocking.
