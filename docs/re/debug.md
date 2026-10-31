# Debug tool: warps, flags, god mode

Tool: `tools/debug/warp.lua` + `tools/debug/scenes.lua` (scene list), `tools/debug/regen.py` (every scene from a cold
boot: proof shot `work/qa/scenes/<scene>.png` + state `work/states/<scene>.mss`), `tools/debug/chesc.py` (the
debug chapter-select questions). Addresses are for the `rom.sha1` dump.

```
python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/maer_en.gba --out work/qa/warp --script tools/debug/warp.lua --var "SCENE='ending'" --frames 3000 --sheet
python -X utf8 tools/debug/regen.py [ROM] [--only a,b]
```

## The leftover debug room (verified: all 73 scenes warp from a cold boot, `regen.py`, 2026-11-01; proof shots read)

- **DBG_ESC.SPC** (stored, never chained by the game) sets up a debug save: all flags it needs, 8 party members
  (`PmbStatusInit`), a deck, Babbo, and puts the player on map `AD0_R_3A`, a room with 14 NPCs.
- Talking to any NPC there runs **S_CHRIRQ.SPC**, which chains **CH_ESC.SPC** when the field is `AD0_R_3A`.
  CH_ESC is a debug chapter select: `GetIrqCause` (which NPC) -> switch at 0x4495 -> each NPC asks yes/no questions
  in turn (`MswStr`, `PopMenu`, jump to a switch whose case 1 is the "yes" block). 40 questions, listed by
  `tools/debug/chesc.py`: start / skip opening, every story stage (Loup-Garou, Paz, ice castle, Pelica, the gates,
  Rubelia, Vestry, the three dungeons, each Talos fight), ending (END2.SPC), staff roll only (SROLL.SPC), towns
  without events, all party members usable, full items/ÄRM (FULL_ITM.SPC), a portrait viewer (DBG_FACE.SPC) and the
  engraver (Berini) menu. Each yes block sets party/flags itself before it chains the event script.
- One question chains `BTLTEST.SPC`, which is not in the archive: left out of the scene list.

## How warp.lua gets there

1. Mash START/A through the title until the new-game lookup of `OPEN.SPC`: `0x0807AC3C(r0 = package, r1 = name)`
   is the file lookup (`docs/re/nfp.md`); the script loader is `0x080050A8` (lookup, then LZ77 unpack into a heap
   buffer; `0x080050D2`: r4 = unpacked SCRP).
2. Replace r1 (via `emu.setState`) with the target name, written NUL-terminated at **0x0203FF00** (EWRAM that was
   zero in all 18 RAM dumps taken over several scenes; only read during the lookup call). The directory's own name
   field can't be used: 12-character names have no NUL and the lookup fails (returns 0).
3. Kinds: `script` = run that script instead of OPEN.SPC; `chesc` = run DBG_ESC.SPC, walk up and press A, and when
   CH_ESC.SPC has been unpacked write `11 <yes block>` (jump) over its first instruction (buffer + 22); `npc` = run
   DBG_ESC.SPC, then the named script in place of CH_ESC.SPC (NPC context: shops, `W_MAP.SPC`, `S_DUNG.SPC`).
4. Options: `route` (inline route after the warp), `mash`/`mash_until` (A every N frames), `wait` (frames after the
   warp for the proof shot), `gen` (dungeon gate), `unlock` (title modes), `kill` (game over), `flags`/`vars`.

## Game state (verified by disassembly of the natives; the field HP by poke)

- Native table: { u32 name pointer, u32 Thumb function } pairs around 0x081ACB90-0x081B0280 (e.g. `SetBool` at
  0x08005B6C, `SetVar` 0x08005B90, `AllHpRecover` 0x08012E58, `GetPlayMode` 0x08012794). Natives take r1 = argument
  array, r2 = result pointer.
- **G = [0x03003FDC]** (0x020360C4 in the runs seen): story flags bit n at G+0xAC+(n>>3), bit n&7 (`SetBool`);
  vars u32 at G+0x2C+4n (`SetVar`); play mode u16 at G+0x4258; party records G+0x35E0+0x54*i (i<8): +2 HP s16,
  +4 max HP. `scenes.lua`: `S.set_flag`, `S.set_var`, `S.god`.
- **Battle**: B = [0x03004020], unit stride 0x688, unit 0 = leader. The leader's HP lives in four copies, all of
  which must change: u32 B+0x228 (setter 0x080096D8), u32 B+0x22C (bar, eased by 0x08009420), u32 B+0x604, u16
  B+0x3A6 (found by RAM search + write watch in the Loup-Garou fight). Zeroing all four gives GAME OVER
  (`game_over` scene); GOD=1 restores them to the highest value seen.
- **Dungeon gate**: `DungGetGenNo` (0x0801263C) returns [D+0x618], D = 0x08070090(); warp.lua forces r0 at
  0x0801264C. `S_DUNG.SPC` (dungeon-mode entry) with gen 0-4 gives 修練/練磨/鍛錬/練武/最後の門 BF1.
- **Title modes**: ÄRM交換/対戦/ダンジョン are locked without a cleared save. Mode-list init 0x08052F44 (r6 = title
  work, 0x02014B24 seen) enables modes 1-2 if u32 [r6+0x7A8] != 0, mode 3 if [r6+0x7B4] != 0; list values at
  r6+0x7B8, count r6+0x7CE, cursor r6+0x7C8. Even unlocked, ÄRM交換 shows no lit sprite and pressing A on it shows
  nothing new (needs a link partner?); 対戦 opens PARTY SELECT (通信対戦), ダンジョン its sub-menu.
- SRAM is read once at boot (0x0E000000 = 0xFF on a blank save -> no data). The staff roll ends on CLEAR PASSWORD
  (「SNOW PRINCESS」) and returns to the title without writing SRAM.

## Not reached yet (add when a phase needs them)

Link-cable screens past PARTY SELECT (つうしん... messages), the password entry screen, the save prompt (セーブ;
`SysMenuExec` in W_MAP/shops), the CH_ESC question about `BTLTEST.SPC`.
