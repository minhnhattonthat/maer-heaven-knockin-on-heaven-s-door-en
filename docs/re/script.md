# SCRP event scripts (*.SPC)

Tool: `tools/scrp.py check|dis OFFSET` (`check` exits 1 on any parse error or bad jump target).

## Container (verified: all 334 SPC files parse)

`SCRP` u32 size, then chunks `tag` u32 size data:
- `CODE`: u16 0x0400, u32 locals count, then bytecode. **Code offsets in operands are relative to CODE data +6**
  (`CODE_BASE` in `scrp.py`).
- `FUNC`: native-function import fixups: repeated { name NUL, u32 offset..., u32 0 }. Each offset points at the u32
  operand of a `0x80` call instruction (offset - 1 is the opcode; checked 25221/25221). 104 natives, e.g. `MswStr`,
  `MswHit`, `BgmPlay`, `ChrMove`, `exec`, `chain`, `PopMenu`.
- `NVAR` (1 file, G_EV023.SPC): not decoded; unlike the others its size field counts its own 8-byte header.
- Every file ends with a bare `TERM` tag (no size); the `SCRP` size field = file length - 8.
- `scrp.rebuild(script, {pos: new string})` re-emits a script with strings changed and every jump/switch target,
  `0x22` string address and FUNC fixup relocated (verified: identity on all 334, and lengthen-every-string then
  restore gives the original bytes; `tests/test_build.py`).

## Instruction set (verified: linear parse ends exactly at CODE end in all 334 files, and every jump target of
0x11/0x12/0x15 lands on an instruction start; 0 bad targets)

Operand bytes per opcode (`OPS` in `scrp.py`): 00:0, 10:str, 11:4, 12:5, 15:switch, 20:2, 21:5, 22:5, 28:1, 29:4,
2a:1, 30:2, 31:5, 32:2, 33:5, 35:5, 37:5, 39:5, 3a:1, 40:2, 50:2, 52:2, 54:1, 58:1, 5a:1, 5b:1, 5c:1, 70:3, 72:2,
73:2, 78:2, 79:1, 80:4, 8f:0.

| Op | Meaning (how proven) |
|---|---|
| 10 | inline string: u16 length (incl. NUL), Shift-JIS bytes, NUL. Executed as a skip. |
| 22 00 u32 | push address of a string: the u32 is the offset (rel. CODE_BASE) of the string bytes of the **immediately preceding** `10` (verified: 10035/10035 strings, every `10` is followed by its `22`) |
| 11 u32 | jump (target rel. CODE_BASE; verified) |
| 12 u8 u32 | conditional jump (verified) |
| 15 u8 n {u32 value, u32 target}*n | switch (verified) |
| 80 u32 | call native; operand fixed up via FUNC (verified) |
| 29 u32 | push immediate (guess; values are small ints) |
| 31 0f u32 | pop/drop n bytes after a call (guess) |
| 8f | return/end (guess) |

**Relocation rule for insertion** (phase 4/5): changing a string's length shifts code, so rewrite every 0x11/0x12/
0x15 target, every 0x22 string address and every FUNC fixup past the change. Unknown: whether any `0x29` push
carries a code offset (e.g. an argument to `exec`/`chain`); 905 pushes coincide with string addresses but none
are next to their string, so they look like coincidences. Safer alternative: keep code in place and append the
English strings after CODE (repoint only the `0x22` operands); decide in the phase 5 engine spike, and check the
EWRAM script buffer size (largest decompressed script 33 414 bytes; destination seen 0x02000F40).

## Text in scripts (verified by decode)

- 10 035 strings: 5 563 display strings (3 199 unique, 119 497 bytes) and 4 472 identifiers (file/label/flag names
  such as `F01B01`, `DITEMCOM.SPC`, `TAKARA`, `A`) that must not be translated.
- One string = one line; a message box is built from several pushes and a native call. Speaker names are their own
  string, e.g. ` C0D04 ［エド］ C0F04 `.
- Longest display line: 21 full-width characters (ignoring control codes).
- Control codes in text: see `text.md`.
