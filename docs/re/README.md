# Reverse-engineering notes

One file per subsystem (text engine, pointers, compression, font, graphics). Mark every finding with how far it is
proven, so a later session doesn't build on a guess:

- **verified** - and how: a decoded known string, a corrupt-and-boot test, a breakpoint hit on the drawing path, a
  passing roundtrip test. Name the test or savestate.
- **guess** - and why it seems likely (byte pattern, another game, an earlier patch's notes). Promote it to verified
  before code depends on it.

Addresses are for the dump in `rom.sha1` unless a note says otherwise.

| File | Covers | State |
|---|---|---|
| [nfp.md](nfp.md) | ROM map, free space, MAR.NFP archive (all game files by name), file kinds | archive verified; free space partly checked |
| [script.md](script.md) | SCRP event-script bytecode, string ops, relocation rule | opcode lengths + jumps verified (`tests/test_formats.py`) |
| [text.md](text.md) | Shift-JIS encoding, control codes, FONT.NFT 8x8, where all text lives | encoding/font verified; control codes guessed |
| [debug.md](debug.md) | debug room + chapter select (CH_ESC), warp method, game-state/battle/dungeon/title-mode RAM | warps verified (`tools/debug/regen.py`) |
| [graphics.md](graphics.md) | graphics-text survey: every tile-drawn Japanese element | static sweep + boot tour |

Prior work: no earlier fan translation or community tools found (web search 2026-10-31: romhacking.net mirrors,
general search). Compression: BIOS LZ77 only (`tools/gbalz.py`, roundtrip-tested); no Huffman seen.

Recon tools: `tools/gbalz.py` (LZ77 codec + scan), `tools/nfp.py` (archive list/extract), `tools/scrp.py`
(script parse/disassemble/check), `tools/gfxsweep.py` (static graphics sweep), Lua probes `tools/lua/pkglog.lua`
(file lookups by name), `tools/lua/lzlog.lua` (who reads a block).
