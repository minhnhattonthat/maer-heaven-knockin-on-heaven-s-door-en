# MÄR Heaven: Knockin' on Heaven's Door (GBA) English translation

Skill: translate-retro-game; `python tools/skill.py` prints its folder (`$SKILL` below). Read its SKILL.md and `references/platform-gba.md` before ROM, text or QA work. `"$(python tools/skill.py)"` works in bash and PowerShell; never paste a `plugins/cache/<hash>` path.

## Commands (run from repo root)
- Build:    `python -X utf8 tools/build.py` -> `build/maer_en.gba` (checks the dump against `rom.sha1` first; no edits = byte-identical, `tests/test_build.py`)
- Check:    `python -X utf8 tools/check.py` (tests + lint; the pre-commit hook runs this)
- Smoke:    `python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/maer_en.gba --out work/qa/smoke --route tools/routes/boot.txt --smoke`
- Warp:     `python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/maer_en.gba --out work/qa/warp --script tools/debug/warp.lua --var "SCENE='<name>'" --frames 3000 --sheet` (scenes: `tools/debug/scenes.lua`, how: `docs/re/debug.md`; `--var GOD=1` god mode; never ask the user to play to a scene)
- States:   `python -X utf8 tools/debug/regen.py [ROM] [--only a,b]` (every scene from cold boot -> `work/states/<scene>.mss` + `work/qa/scenes/` shots; rerun after code/font/graphics changes)
- Release:  `python -X utf8 tools/release.py` (patch + verify; never publish without the user)
- Clean:    `python -X utf8 tools/clean.py` (published projects: lists rebuildable/downloadable files; `--yes` deletes)
- Hooks:    `git config core.hooksPath tools/hooks` once per clone (pre-commit runs the check).

## Paths
- Original ROM: `rom/MAER Heaven - Knockin' on Heaven's Door (Japan).gba` (16 MiB, game code BM9J, gitignored; SHA-1 in `rom.sha1`, checked by `tools/check_rom.py`).
- Emulator: this repo's own MesenCE in `tools/mesen/` (release 2.2.1, https://github.com/nesdev-org/MesenCE/releases/download/2.2.1/Mesen_2.2.1_Windows.zip; GBA BIOS `tools/mesen/Firmware/gba_bios.bin` via `fetch_emu.py gba-bios`; gitignored; settings in `tools/emu-config/`). Savestates: `work/states/`.
- Text: `script/` (format decided in phase 4). Tables: `tbl/`. Glossary: `glossary.md`. RE notes index: `docs/re/README.md`. Fonts and their licences: `docs/fonts.md`.
- Build-time copies of skill scripts: `tools/tbl.py`, `tools/bps.py`, `tools/romdiff.py`. QA tools (`emu.py`, `play.py`, `qa_gate.py`, `jp_left.py`) run from `$SKILL/scripts/`.

## Rulings
- Edit source files (.py .lua .asm .tbl .json) only with the file-edit tool; scripts here read and analyse, never `.replace()` and write back.
- Subagents: dispatch the `.claude/agents/` types (translator, reviewer, visual-qa, playtester), never general-purpose: their short tool list cuts each agent's start-up context from ~43k to ~9k tokens.
- The user's decisions, with the options and reasons: `docs/decisions.md`. Read it before asking the user anything; add each new ruling there the same session.
- Player bug reports: GitHub issues (`gh issue list --label bug`). Copy the attached save into `work/states/`, reproduce in the emulator, fix, commit with `Fixes #N`, and update `docs/status.md`.
- ROM is 16 MiB (max size) with non-padding bytes up to 0xFFFF00: the ROM can't grow; free space must be found inside it (phase 1, `docs/re/`).

## Status
`docs/status.md`: done, next, open bugs. Update it at the end of every session.
