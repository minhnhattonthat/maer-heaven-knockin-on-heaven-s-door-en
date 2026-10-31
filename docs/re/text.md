# Text encoding, font and text locations

## Encoding (verified: decoded strings match the opening scene on screen, e.g. 「つかれたぁ」, 「ＡＲＭよ　いざなえ！！」)

Shift-JIS (cp932), NUL-terminated. Plus the font's own user-defined glyphs in the 0xF0xx range: e.g. `F0 56`
(cp932 U+E016) = the "Ä" of MÄR, written before `ＲＭ` (「ＲＭ」 shows as ÄRM on screen).
No table file needed: `jp_left.py --sjis` works directly. ASCII inside display text appears only in control codes.

## Control codes (inline ASCII; **guess** from usage, confirm in the phase 5 renderer RE)

| Code | Count | Seen as | Guess |
|---|---|---|---|
| ` C0F04 ` | 2209 | after a name, before normal text | colour: default text colour (C + 2 hex colour + 2 hex ?) |
| ` C0D04 ` | 2160 | before `［name］` | colour: speaker-name colour |
| ` C0904 ` | 75 | around key words/numbers (「 C0904 ２０ C0F04 こまで」) | colour: highlight |
| ` C0B04 ` | 20 | 「 C0B04 う C0F04 」 | colour: another highlight |
| `T0000 ` | code strings | `T0000 C0905 %s` in literal pools | unknown (text position/speed?) |
| `%s` `%d` | code strings | printf | runtime-built strings (e.g. 「%s　ＧＥＴ！！」) |

The leading and trailing spaces are part of every code as stored (with 3 exceptions without them in
DITEMCOM.SPC); keep the bytes exactly in extraction (roundtrip test) until the parser is read.

## Font (verified: FONT.NFT render, font read-watch during dialogue)

`FONT.NFT` (MAR.NFP, ROM 0x7BA990): header `NFT Ver1.0 (c)2001 NOBODY`, +0x20 width 8, +0x24 height 8,
+0x28 bpp 1, +0x2C glyph count 7984, +0x30 palette offset 0x40, +0x34 glyph data offset 0x60, +0x38 8 bytes per glyph.
Glyphs are in JIS X 0208 order (94 per row: row 1-2 symbols, row 3 digits and **full-width Latin A-Z a-z**, row 4
hiragana, row 5 katakana ...; index ≈ (ku-1)*94 + (ten-1)), then the user-defined glyphs. Every glyph is drawn in an
8x8 cell, full-width and Latin alike: English with the existing font is 8 px per letter, fixed width.
Drawn by ARM code at 0x08000800-0x08000D40 (reads the glyph rows; seen at frame 2075+ of the opening).
Dialogue box: 26 cells of 8 px across (x 16-224), lines 8 px apart; widest Japanese line is 21 cells. **Width gate
and VWF decision: phase 5.** Whether single-byte ASCII is drawn (half-width) is not known yet.

## Where the text is

| Source | Size | Pointer form | Notes |
|---|---|---|---|
| Event scripts, 334 SPC files in MAR.NFP | 5 563 display lines, 119 KB | inline in bytecode, addressed by the following `22` op | `script.md` |
| ARM / card records, 0x1B0970-0x1BE7EF | 445 records x 0x80 | fixed records, no pointers | +0x02 8-char ID, +0x0C name (0x22-byte field), +0x2E description (0x22-byte field; verified: longest 32 bytes, zero fill, first stat byte at +0x50), rest stats |
| Item records, 0x1BE7E0 + 0x50*i, i 0-13 | 13 items + record 0 | fixed records | same name/description fields (0x22 each); record 0 has no name and desc 「　」 and its first 16 bytes overlap the last ARM record's zero tail |
| String block 0x87300-0x89537 | 136 JP strings | u32 `0x08xxxxxx` in Thumb literal pools and pointer tables (0x1B0768.., 0x1BECEC.., 0x1BF22C..) | system/menu messages: save/load, shop (ＲＭ屋), elements, 「%s　ＧＥＴ！！」, link-cable messages, party names. Mixed with resource names (`ARM_DA01`, `MAR.NFP`), natives and format strings (`T0000 C0F04 %s`) that must stay. Every JP string has a pointer; one pointer (0x13D884) points 10 bytes into 「キャラクターをえらんでください」 (= 「ーをえらんでください」) |
| Graphics text | - | - | `graphics.md` |

An SJIS sweep of 0x000000-0x1C0920 outside those ranges finds only noise (code bytes that happen to decode).
Phase 4 re-check (verified): a strict sweep (NUL-terminated runs of 3+ full-width chars, half kana) finds nothing
outside the string block and the record tables, and nothing in the non-script archive files (graphics, font).

## Script files (phase 4; `tools/extract.py`, codec `tools/text.py`, tests `tests/test_extract.py`)

`python -X utf8 tools/extract.py` writes `script/` from the original ROM; re-running keeps `en`/`status`/`notes`
per id (a changed `jp` under a translation sets `status: jp-changed`). JSON lists, `indent=1`, UTF-8.

| File | Entries | id | Extra fields |
|---|---|---|---|
| `script/spc/<NAME>.json` (170 scripts) | 5 563 (3 199 unique) | `NAME:<CODE pos of the 0x10 op>` (the `build(edits=)` key) | `call` (always `MswStr`), `box` (index of the call in the file), `line` (push index; line 0 = speaker label, 2 156 of them `{C0D04}［name］{C0F04}`), `speaker` |
| `script/code.json` | 136 | `code:<ROM offset>` | `refs` (pointer locations), `subrefs` (pointers into the middle, by byte offset), `slot` (bytes incl. NUL padding) |
| `script/records.json` | 917 (660 unique) | `arm123.name` / `item005.desc` | `addr`, `max` (bytes before the NUL) |

Text form (`text.py`): Shift-JIS decoded; colour codes ` C0F04 ` -> `{C0F04}` (the 6 with odd spacing stay
literal); user glyphs F040 -> `♥`, F056 -> `Ä`, other user glyphs `{Fxxx}`. Leading/trailing full-width spaces are
text (the opening narration lays out lines with them). Not extracted, by rule: pure-ASCII script strings
(4 472 identifiers incl. two name-less labels ` C0D04  C0F04 `), ASCII strings of the string block, ARM IDs
(+0x02, password characters). Graphics text is separate (`graphics.md`).
Tests: every `jp` re-encodes to the ROM bytes; every script string is extracted iff it has a byte >= 0x80; every
string-block string likewise; record fields hold one string + zero fill; `script/` equals a fresh extraction.
