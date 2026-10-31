# Text renderer, English engine patch and box widths (phase 5)

Tool: `tools/engine.py` (font + hooks, applied by `build.py` whenever English text is present), font source
`fonts/vwf8.txt`, tests `tests/test_engine.py`. Addresses are for the `rom.sha1` dump.

## Renderer (verified by disassembly + marker build)

- Glyph lookup `0x0807AE10(font = 0x030032E4, code)`: Shift-JIS -> FONT.NFT glyph index (`0x0807AE7C`); `F056` ->
  `81FA` (Ä), `F040` -> `81F9` (♥); a **single-byte code b maps to glyph b + 0x1E0** (Greek/Cyrillic slots the
  game never draws). So ASCII 0x20-0x7E needs no lookup change: `engine.font()` puts the English glyphs there.
- Glyph blitter `0x08011688(dst, glyph, x, y, ink, ?, tiles per row)`: 1bpp 8x8 -> 4bpp tiles at **any pixel x/y**
  (8 ARM variants for x & 7 at 0x0800080C.., table 0x081AFE84). A VWF only has to change the callers' x step.
- The font's 5 users (all via 0x030032E4):

| Caller | What | x step |
|---|---|---|
| 0x08011870 | MswStr dialogue window task (VRAM 0x0600C020, 24 tiles/row, 3 lines 11 px apart, y = line * 11 + 2, shadow at +1,+1) | x = (col / 2) * 9, col += 2 per glyph |
| 0x0801B95C | one fixed string (0x08087468 キャラクターをえらんでください), centred | x - strlen/2 * 4, 8 px |
| 0x0801E168 | centred string (r0 str, r1 centre x, r2 y), VRAM 0x06008000 | 8 px |
| 0x080532A4 / 0x080533F0 | list/menu windows: string arrays, x = base + (byte index / 2) * (spacing + 8) | 8 px; 0x8260 (Ａ) is drawn as Ä |

- Dialogue text fetch `0x08011AF4`: Shift-JIS pairs are glyphs; single bytes: `C`/`c` + 4 hex = colour,
  `T`/`t` + 4 hex = timing, NUL = next line (3 lines; line 0 is the speaker label), anything else skipped. Line
  buffers 0xA1 bytes each (strcpy at 0x08011828), line index byte at window+0x1E3 (signed), x at +0x1E4.

## Engine patch (verified: marker build, OPEN.SPC narration box, `work/qa/m_new`)

- Font: `fonts/vwf8.txt` (drawn for this project): caps rows 0-6, x-height rows 2-6, descenders row 7; advance =
  glyph width + 1 (the shadow fills the gap). 2-byte glyphs keep 9 px.
- Hook `fetch` (0x08011B2E -> free space): printable single bytes go to the glyph path; C/c/T/t are codes only
  when 4 hex digits follow (so English "Cafe!" is text; a word like "Cabbed" would be a code: lint it).
- x = window+0x1E4 as a pixel byte (0x08011936); hook `adv` (0x08011990): x += advance, index += 1 or 2.
- English encoding (`text.encode_en`): ASCII single bytes, `{C0F04}` -> `C0F04` with no spaces, other characters
  Shift-JIS (`Ä` = F056, `…` = 8163, 9 px).
- Hooks sit at 0xFE4000 (0xFF fill 0xFE4000-0xFFF000; 0xFE3090-0xFE3FFF is zero, part of the library block, not
  used). Thumb BL reaches only +-4 MiB, so game code jumps out with `ldr r0,[pc]; bx r0` and hooks jump back.
  `engine.asm` rejects any 32-bit Thumb-2 encoding keystone picks.

## List windows, labels and byte-count layout (verified: build/widthtest.gba --code-test, 2026-11-01)

- `measure` (list x, centred labels): ASCII adds its advance only (the window's per-glyph spacing, 1 px in the
  status/name windows, would leave 2-px gaps; the advance already holds the shadow gap); 2-byte glyphs keep
  8 + spacing, so Japanese strings lay out exactly as before. `engine.list_width()` mirrors it.
- **Pad bytes** 0x01-0x1F: blank glyphs (FONT.NFT slots 0x1E1-0x1FF cleared) that advance their own value in px
  in list windows and centred labels (`{p5}` in English text; the dialogue skips them). The build pads strings of
  a `pad_to` window (`script/windows.json` 'code') to that exact width, so the digits the game appends line up.
- **Status rows**: the status screen builds each row in a 25-byte buffer (0x020138C4 + 0x19 * row): label strcpy,
  then 2 bytes from each digit string (０-９, ／): those must stay 2-byte glyphs (`keep` window); label + pads +
  digits + NUL must fit 25 bytes (`bytes` in windows.json).
- **pxlen**: 10 places size text by byte count (`len / 2 * 8` px): name tab right-aligned in 7 cells
  (0x08053C2C, 0x08053D7E: x = base + (14 - len) / 2 * 8), names centred in 104 px (0x0805AF04, 0x0805B108,
  0x080641A0, 0x080643AA, 0x0806BBC2, 0x0806BE1E), area names centred in 128 px (0x0806D7CA, 0x0806D810). Their
  `bl strlen` now goes through a veneer at 0x0801B988 (dead code after the 0x0801B97C rewrite) to the `pxlen`
  hook: an even length whose len / 2 * 8 = measured width rounded up to 8 (Japanese: the byte length). Text
  can sit up to 7 px off (right-aligned) / 3 px (centred). Other strlen users are loop counts or strcat.
- Renderer per code string: `tools/lua/drawlog.lua` + `tools/debug/drawmap.py` -> `work/qa/drawmap/map.tsv`.

## Script size rule (verified: OPEN.SPC crashed at +1 code byte past a 4-byte step)

The VM (`0x0807E4C4`) copies CODE (size - 6, plus a 0x400 stack) into a heap block (heap at 0x02028010,
~48 KB free in the opening) and writes the stack top word-aligned. All 334 original CODE sizes are 2 mod 4; a
size off that step overwrites the next heap block's header and the next allocation crashes (black screen).
`scrp.rebuild` NUL-pads the last changed string so the total change is a multiple of 4 (assert). LZ77 scripts are
also unpacked into heap 0x02000000 (64 KB, 61 KB free at the opening); heap logging: `tools/lua/heaplog.lua`
(`--var ALLOCS=1` for every allocation), buffer writers: `tools/lua/wwatch.lua`.

## Box widths (width gate)

See `script/windows.json` (px per line, lines per box) and the shots named there.
