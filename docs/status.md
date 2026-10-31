# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 1 (research and recon) done -> next is phase 2 (debug tool). Last build: none yet (2026-11-01).
- **Done:** Step 0 (MesenCE 2.2.1 + BIOS, `rom.sha1`, pre-commit check). Phase 1, all in `docs/re/`:
  - no earlier fan patch or community tools exist;
  - all game files live in the **MAR.NFP** archive (0x1C0920-0xF28406, 830 files looked up by name): `tools/nfp.py`;
  - text is Shift-JIS + inline ASCII colour codes (` C0F04 `); font `FONT.NFT` is 8x8 1bpp in JIS order with full-width Latin;
  - story text = 334 SCRP bytecode scripts (5 563 display lines), opcode table and relocation rule verified: `tools/scrp.py check`;
  - item/ARM records at 0x1B0970 (445 x 0x80, fixed fields); ~138 system strings in code literal pools 0x87468-0x8A000;
  - compression BIOS LZ77 only: `tools/gbalz.py` (roundtrip test);
  - free-space candidates 0xF2B448-0xFDFFFF (723 KiB) and 0xFE3090-0xFFF7FF (110 KiB), no reads seen on the boot/opening tour;
  - graphics-text survey (static sweep of every BG, tile set and 9 252 sprite frames): `docs/re/graphics.md`.
  - tests: `tests/test_formats.py` (LZ77, NFP directory, script parse, string/push pairing).
- **Next:** phase 2 debug tool (`tools/debug/warp.lua` + `scenes.lua`): find the script runner / scene-load call so a warp can load any `*.SPC` by name (the loader is `0x080050A8`, lookups `0x0807AC3C(pkg, name)`; `tools/lua/pkglog.lua` logs them), story flags (`SetBool`/`GetBool` natives), god mode; scene list must include every dungeon gate, title cards, credits (SYSTEM.NCD 1698-1781), game over. Then phase 3: identity rebuild of MAR.NFP + scripts.
- **Open questions for later phases:** single-byte ASCII support in the text renderer (ARM blitter 0x08000800-0x08000D40); exact meaning of `C`/`T` codes; whether any `0x29` push carries a code offset (append-strings strategy avoids it); EWRAM script buffer size.
- **Open bugs:** none.
- **Waiting on the user:** GUI keyboard input in `tools/mesen/Mesen.exe` not checked by a human (headless only). Non-blocking.
