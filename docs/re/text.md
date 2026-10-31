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
| Item / ARM / card records, 0x1B0970-0x1BE7EF | 445 records x 0x80 | fixed records, no pointers | +0x02 8-char ID, +0x0C name (0x22-byte field), +0x2E description (0x30-byte field), rest stats. More tables follow up to ~0x1BEC1E (not yet decoded) |
| Literal-pool strings 0x87468-0x8A000 | ~138 JP strings | u32 `0x08xxxxxx` in Thumb literal pools | system/menu messages: save/load, shop (ＲＭ屋), elements, 「%s　ＧＥＴ！！」. Mixed with resource names (`ARM_DA01`, `MAR.NFP`) that must stay |
| Graphics text | - | - | `graphics.md` |

An SJIS sweep of 0x000000-0x1C0920 outside those ranges finds only noise (code bytes that happen to decode).
