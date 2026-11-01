# MÄR Heaven: Knockin' on Heaven's Door English translation

Unofficial English fan translation of **MÄR Heaven: Knockin' on Heaven's Door** (Game Boy Advance, Konami, 2005): the source text and tools
that build the patch.

**Just want to play?** Download the patch from [Releases](../../releases) and follow its README. This repository holds
no game data you can play; you need your own dump of the Japanese game.

**Found a bug?** [Report it](../../issues/new/choose): untranslated text, typos, overflow, crashes. Attaching a savestate
helps most.

## Translation status

| Part | Status |
|---|---|
| Dialogue / story | Translated (all 12 chapters, story-pass reviewed) |
| Menus, items, ÄRM, system messages | Translated |
| Mode screens, logos, graphics with text | Translated (redrawn) |
| Title screen logo | Left in Japanese (original art kept by choice) |
| Credits roll | Translated (names romanised) |
| Debug chapter select (not reachable in normal play) | Left in Japanese |

Known issues: see [Issues](../../issues). A few graphics with text (area name cards, recipe/password prompts,
link-cable messages) were only checked in a preview, not in game.

## What's here

| Path | What it is |
|---|---|
| `script/` | Every text block: original Japanese and English. Translation fixes go here. |
| `glossary.md` | Binding names, terms and style rules. |
| `tools/` | Python build chain: extract, insert, lint, release. |
| `tests/` | pytest suite (ROM-dependent tests skip when the ROM is absent). |
| `docs/re/` | Reverse-engineering notes. |
| `docs/decisions.md`, `docs/status.md` | Rulings with their reasons; current progress and open bugs. |
| `docs/fonts.md` | Fonts used and their licences. |
| `AGENTS.md` | Instructions for coding agents (`CLAUDE.md` points to it). |
| `.claude/agents/` | Subagent types (translator, reviewer, visual QA, playtester) with only the tools each needs. |

## Build your own patched ROM

Needs Python 3.12+ and your own dump of the Japanese game.

```sh
git clone https://github.com/minhnhattonthat/maer-heaven-knockin-on-heaven-s-door-en
cd maer-heaven-knockin-on-heaven-s-door-en
# copy your dump to: rom/MAER Heaven - Knockin' on Heaven's Door (Japan).gba
#   (16777216 bytes, SHA-1 5ed178bfbdf459867d64e5b91a9d9c72654e4051; the build refuses any other dump, see rom.sha1)
python -X utf8 tools/build.py                          # -> build/maer_en.gba
python -X utf8 tools/check.py                          # tests + text lint
```

## Support

If you enjoy this translation, you can support my work on Ko-fi:

[![Support me on Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/minhnhattonthat)

## Licence

Tools and English translation: MIT. The original Japanese text in `script/` is Konami's and is included only so
the translation can be checked against it. MÄR Heaven: Knockin' on Heaven's Door is (c) Nobuyuki Anzai / Shogakukan / ShoPro / TV Tokyo / Konami; this project is not affiliated with them.
Do not share patched ROMs.

The translation was made with extensive AI assistance (Claude by Anthropic). Corrections are very welcome.
