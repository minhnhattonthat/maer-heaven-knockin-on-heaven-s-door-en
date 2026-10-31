# Decisions

The user's rulings on scope, style and trade-offs, newest last. Read before asking the user anything; if a later
decision replaces one, mark the old one "replaced by D<n>" instead of deleting it. Binding term spellings live in
`glossary.md`; this file holds the why.

Source for D1-D7: the owner's standing answers injected into the one-shot run brief (Orca coordinator), 2026-10-31.

| # | Date | Question | Options offered | Decision and reason |
|---|---|---|---|---|
| D1 | 2026-10-31 | Honorifics and name order | keep (-san), drop; JP or Western order | Keep honorifics; Western order (given name first). Owner's standing answer. |
| D2 | 2026-10-31 | Romanization source for names | official art, earlier patch, Hepburn | Official English names where they exist (Viz manga / English anime "MÄR"), else an earlier fan patch, else Hepburn without macrons. |
| D3 | 2026-10-31 | Credits | stay Japanese, translate | English. |
| D4 | 2026-10-31 | Abbreviations | engine work first (default), abbreviate | Default: engine work first (VWF, wider boxes, relocation); abbreviate only as a flagged last resort. |
| D5 | 2026-10-31 | Graphics text left in Japanese | none (default), list | Translate all (titles, menus, banners, cards); keep the original Japanese logo only if it has no official English version. |
| D6 | 2026-10-31 | Specs and plans | need approval, pre-approved | Pre-approved: keep going through checkpoints, report at the end. |
| D7 | 2026-10-31 | Existing saves / savestates | user supplies, none | None provided; build the debug tool as usual. |
| D8 | 2026-10-31 | Git identity | - | Already set by new-game.ps1 (minhnhattonthat); don't change it. |
| D9 | 2026-11-01 | Register, spelling, SFX (phase 6; controller's default under D6, not asked) | formal/casual; US/UK | Upbeat kid-friendly shonen, American spelling, SFX as interjections. Matches the kana-for-kids source. Owner may override. |
| D10 | 2026-11-01 | Speaker labels (controller's default under D6) | ［Name］ kept as [Name]; bare name | `[Name]` in the label colour, like the Japanese ［］. |
| D11 | 2026-11-01 | Game-original / uncertain names (controller's default under D6) | Hepburn; English-ised | Marl (マール, avoids "Mar"/MÄR clash), Bellini (ベリーニ), Luberia, Paz Town, Pazurica, Orco, Girom, Luga & Garu; marked UNSURE in glossary.md for the owner to check. |
| D12 | 2026-11-01 | Verbal tics without a JP-style English equivalent (controller's default under D6) | drop; English device | Jack っス -> folksy drawl (dropped g's, "y'know", "Ma"); Bellini ですのん -> ", nonn"; Nanashi Kansai -> breezy slang. docs/style-reference.md. |
| D13 | 2026-11-01 | ÄRM type tags 攻/防/攻防/回復/特殊 in 16x16 / 32x16 sprite cells (controller under D4, flagged last resort) | full words (no room); abbreviate | AT, DF, A+D, HEAL, SPEC: the cells hold 2-4 small letters; widening would overlap the list. Owner may override. |
| D14 | 2026-11-01 | Sprite lettering font (controller under D6) | downscaled TTF; pixel font | Pixelify Sans (OFL) Medium at 13/11 px without antialiasing, our vwf8 for 8-px labels; colours cloned from each original frame (`tools/gfxtext.py`). |
| D15 | 2026-11-01 | Staff-roll names and roles (controller under D2/D3) | keep kanji; romanize | Given name first, Hepburn without macrons, roles as English credit terms, 小学館プロダクション = "ShoPro" after a name (as in the game's copyright line); Shogakukan org lines in the small font (mid doesn't fit the screen). Readings guessed from kanji, owner may correct: 幹 Motoki (Uchiyama), 文 Aya (Ito), 匡 Tadashi, 信 Makoto (Murato), 昇 Noboru, 汾陽 Kawaminami, 樹下 Kinoshita, 備前島 幹人 Bizenjima Mikito, 佳代子 Kayoko, 加奈代 Kanayo, 洋 Hiroshi. |
| D16 | 2026-11-01 | Title logo メルヘヴン (owner ruling) | keep the art; redraw in English | Owner: keep the original Japanese title screen untouched (the redraw was "ugly"); all T_TTL06 rows deleted, katakana reading under the subtitle kept too. Superseded controller ruling: the colour katakana covered the lower half of the official silver MÄR art, so the top 80 px are a new two-line logo, silver "MÄR" over "HEAVEN" in the katakana's fire colours (Pixelify 45/39 px, `gfx/BG.tsv`); English subtitle lines kept, the small katakana reading under them removed. Owner may prefer the original art (delete the T_TTL06 rows). |
| D17 | 2026-11-01 | COMMAND menu labels 0701-0706 (owner feedback) | Pixelify centred; own bold caps left-aligned | Owner: Pixelify labels hard to read, unlike the original, should be left-aligned. Now a hand-drawn 2-px-stroke caps font (`gfxtext.mask_menu`, `font=menu`), left-aligned at the Japanese ink start, red fill + white outline cloned from the frame. |
