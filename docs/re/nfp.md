# MAR.NFP file archive and ROM map

Tool: `tools/nfp.py list|extract`. Addresses are ROM offsets in the `rom.sha1` dump.

## ROM map (verified: archive parse, `tools/scrp.py check`, emulator lookups)

| Range | What |
|---|---|
| 0x000000-0x1C091F | code (Thumb + some ARM, e.g. glyph blitter 0x08000800-0x08000D40) and data: literal-pool strings (`text.md` §Code strings), item/ARM record table 0x1B0970 |
| 0x1C0920-0xF28405 | **MAR.NFP** archive: 830 named files, every script, graphic, map and the font |
| 0xF28406-0xF2B447 | data referenced from code (pointers 0x08F28410.., e.g. from 0x0019C4); not free |
| 0xF2B448-0xFDFFFF | 0xFF fill, 0xB4BB8 bytes (~723 KiB): **free-space candidate** |
| 0xFE0000-0xFE308F | ARM code + data (library; 15 pointers from code into it); not free |
| 0xFE3090-0xFFF7FF | 0xFF fill (~110 KiB): **free-space candidate** |
| 0xFFF800-0xFFFEFF | data (`c0 ff 09 00` pattern; pointers from code); not free |

Free-space status: **guess, partly checked**. No u32 in the ROM equals an address in 0x08F2B448-0x08FDFFFF except
odd/unaligned values inside compressed data (443 hits, none in literal pools of code that was checked), and a
read-watch over 0x08F2B448-0x08FDFFFF from cold boot through title, main menu, new game and the opening scene
(`tools/lua` + `watch.lua`, route `work/r_newgame.txt`, 2730 frames) logged no reads. Phase 2: a CPU read-watch over 0x08F2B448-0x08FFF7FF during 8 warped scenes (staff
roll to its last page, battle to WIN, a dungeon, ÄRM list, world map, ending, portrait viewer, versus PARTY SELECT;
7000 frames each, `work/qa/free_*`) also logged no reads. DMA reads are not hooked; the identity/insert builds
should still check that nothing breaks when the fill is replaced. The ROM is 16 MiB, so this is the only room.

Save type: SRAM (`SRAM_F_V103` at 0x1AC618).

## Archive format (verified: parse is exact for all 830 entries)

- Header 0x40 bytes at 0x1C0920: `NFP2.0 (c)NOBORI 1997-2002`, then +0x34 u32 count (0x33E = 830),
  +0x38 u32 directory offset (0x40), +0x3C u32 data offset (0x3420).
- Directory: 830 x 16 bytes: name (12 bytes, NUL-padded, 8.3 upper-case) + u32 offset from the archive start.
  Sorted by name, and offsets are ascending in the same order; size = next offset - this offset. The last file
  (`W_MAP.SPC`, LZ77) ends at 0xF28406.
- Files are stored raw or BIOS-LZ77 (type 0x10; `tools/gbalz.py`, first byte 0x10).
- Lookup is by name at run time: `0x0807AC3C(pkg_name, file_name)` -> pointer, via package slots at
  `[0x03006114]` (24-byte slots, +0x10 = package base) and `strcmp` 0x0808280C. Logged with `tools/lua/pkglog.lua`
  (e.g. `MAR.NFP / OPEN.SPC` at frame 1861 of the new-game route). Because lookups go through the directory, a file
  can be moved or resized by rewriting the archive (and its directory) with no other pointer changes (verified
  phase 3: see §Rebuild).
- File size is implicit: `0x0807AD4C` returns next entry's offset - this one (last file: package slot +0x14). Its
  only caller (0x080031EC) loads the KCG/KCL named in a KMP header, so raw tile/palette sizes depend on layout.
- Script-side loader: `0x080050A8` gets the file, checks the first byte for `S` (stored SCRP) else LZ77-unpacks it
  into EWRAM (`0x0807A2EC`; seen with destination 0x02000F40).

## Rebuild (phase 3; `tools/build.py`, `nfp.unpack/pack`, `tests/test_build.py`)

- Every file starts 16-aligned from the archive start, zero fill; the last file is not padded. LZ77/SCRP files are
  trimmed to their real length on unpack, raw files keep their slot. No edits -> byte-identical ROM (test).
- Our LZ77 (`gbalz.compress`, greedy) packs worse than the original packer (all scripts: +8 005 bytes) and is not
  byte-identical, so unchanged files keep their original stored bytes.
- The archive had 0 slack before the fixed block 0xF28406-0xF2B447. When it grows, `pack` jumps that block: the
  rest continues at 0xF2B450 (up to 0xFE0000), the jump placed right after an `.SPC` so no raw file's implicit size
  changes. **Verified**: `build.py --recompress` (every LZ77 script re-packed by us, 20 files incl. W_MAP.SPC and
  the WM_BG/T_TTL06 graphics moved past the gap) passes smoke and warps 73/73 scenes with the same screens as the
  original (diffs only animation frames; `work/qa/rc_scenes/`, 2026-11-01).
- SYSTEM.NCD (1.3 MB raw) sits just before the fixed block, so the jump only buys the ~90 KB after it. When the
  layout doesn't fit, `pack(late=nfp.LATE)` stores `MAP42_A.KMP` (231 KB, directory predecessor `MAP41_A.SPC`)
  last, past GAP, out of name order: the directory stays sorted by name, `entries` sizes files by the next offset
  in data order. **Verified** 2026-11-01: `pkglog.lua` on the `pelica_free` warp shows `MAP42_A.KMP` fetched from the
  spill and the map draws as before.

## File kinds

| Ext | n | What |
|---|---|---|
| SPC | 334 | event scripts (`SCRP`), 92 stored + 242 LZ77; `script.md` |
| KCG / KCL / KMP | 83 / 83 / 193 | BG tiles (LZ77, 4bpp) / palettes (BGR555) / tilemaps (0xC0 header: +0x14 w, +0x18 h, +0x1C KCG name, +0x5C KCL name; then 1-3 layers of w*h u16 GBA text-BG entries) |
| TCG / TCL / TSC | 21 / 22 / 90 | battle BG tiles / palettes / screen maps |
| NCD | 3 | sprite banks `CHR`, `EFFECT`, `SYSTEM` (`graphics.md`) |
| NFT | 1 | `FONT.NFT`, the 8x8 1bpp font (`text.md`) |
