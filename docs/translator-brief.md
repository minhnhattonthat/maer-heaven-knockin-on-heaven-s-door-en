# Translator brief - MÄR Heaven: Knockin' on Heaven's Door (GBA, 2005)

You translate part of the Japanese text of MÄR Heaven: Knockin' on Heaven's Door into English for a fan patch. It is
a card-battle RPG based on the shonen manga/anime MÄR: Ginta, a bespectacled middle-school kid from Tokyo, is pulled
into the fairy-tale world MÄR Heaven, teams up with the talking ÄRM Babbo and friends (Jack, Dorothy, Snow, Alviss,
Nanashi, Ed) and fights the Chess Pieces. Tone: upbeat, funny, kid-friendly shonen; the Japanese is mostly kana
because it is written for children, so keep the English simple and lively, never stiff.
Work only on the batches named in your dispatch, one at a time in the order given, each to a passing check before
the next. Do all translation yourself; do not dispatch subagents.

## Read first
1. `docs/style-reference.md` - character voices and approved example pairs. Match this voice.
2. `build/terms_<batch>.txt` - binding glossary rows for this batch (`JP<TAB>EN<TAB>notes`; full table in
   `glossary.md`). The check fails if a listed JP term is in a line and its English form is not.
3. `docs/synopsis.md` - plot, who is who and the late reveals. Don't give a reveal away early.

## Input: `work/tl/<batch>.tsv`
`id<TAB>speaker<TAB>form<TAB>limit<TAB>Japanese`, in story order (use the neighbours for context).
- form `dlg`: one message box under a speaker label (the label is translated separately); limit `2x192px` = two
  lines of 192 px. `narration`: a box with no label; up to its line count (often 3). ` / ` separates the Japanese
  lines of one box: translate the box as one utterance; English line breaks are made by the tool.
- form `code`: a menu, shop or system message; speaker = its window; limit = px and renderer, plus a note when the
  game puts a price or name in front of the text (then the English must read right after that).
- form `arm_name` / `arm_desc`: ÄRM and item names (112 px, 33 bytes) and one-line descriptions (150 px, 33 bytes).
- `{C0F04}`, `{C0D04}`, `{C0904}`... are colour codes (`{C0D04}` highlight on, `{C0F04}` back to white): keep every one,
  in the same order, around the English words that correspond to the highlighted Japanese. If the Japanese starts
  with a code, the English starts with the same code. `%s` / `%d` are a name / number the game fills in: keep them.
- A box whose Japanese continues in the next box (a sentence cut by a box break): keep it cut at a natural place;
  every box must read on its own as it appears.

## Output: `work/tl/<batch>.out.tsv`, written with your file-write tool (never a shell heredoc)
`id<TAB>English`, every input id exactly once, same order. Plain ASCII: straight quotes, `...`, `--`; the only
non-ASCII characters allowed are `Ä` (always in ÄRM and MÄR) and `♥` (when the Japanese has it). No tabs inside the
English, no Japanese or fullwidth characters, no `\uXXXX`. Normally let the tool wrap; write ` / ` only to force a
line break (e.g. a dramatic pause, or a list).

## Fit and validate
- Dry run: `python -X utf8 tools/batches.py fit "English text" --lines 2` prints each wrapped line's pixel width (a
  dialogue line holds about 40-45 characters). `--list` prints the width for menu/record strings.
- Then `python -X utf8 tools/batches.py check <batch>` from the repo root; fix every reported id until it prints OK.
  A box that doesn't fit must be rephrased tighter (never cut meaning silently); if it truly can't fit, report
  `LONG: id - what had to go`.

## Style
- Faithful: keep the information and order of ideas; adapt idiom, not meaning. Don't add details the Japanese doesn't
  state; don't summarise or skip. Adapt wordplay so the joke still lands (no translator notes).
- Keep the speaker audible. JP register markers carry voice and must turn into English devices, not vanish (see
  the voice table in `docs/style-reference.md`): Jack's っス, Babbo's pompous self-importance, Dorothy's teasing
  ボウヤ, old men's じゃ/のう/わし ("eh?", "my boy"), rough men's ぜ/ねぇ ("ain't", "ya", clipped grammar), feminine
  かしら/わよ/のね ("I wonder...", "you know", "dear"), stretched 〜ぅ/〜っ/～ endings. A line any speaker could have
  said is a mistake.
- Names and terms exactly as in the glossary: ÄRM (never "arm"/"ARM"), MÄR Heaven, Chess Pieces. Never abbreviate a
  name or term to fit (owner's ruling): rephrase the rest of the line instead.
- Honorifics are kept, hyphenated, as the Japanese has them: ジャックちゃん -> Jack-chan, ギンタくん -> Ginta-kun,
  さま/様 -> -sama. Western name order. Don't add honorifics the Japanese doesn't have.
- Punctuation: 「」 -> "...", 『』 -> '...', ・・・/… -> `...`, ！？ -> `!?`, ～ at a line end -> `~` (cheerful
  drawl) or drop it, ♥ stays. Stuttering と、とうぞく -> "Th-thieves?!".
- Placeholders: no suffixes glued to `%s`/`%d` ("No. %d", never "%dth"); no a/an right before `%s`.
- No "... GET!" style calques except where the Japanese is a battle-screen shout.

## Consistency
Never edit `glossary.md`. For a recurring name or term not in it, pick a form, use it consistently, and report it.

## Notes from earlier batches
- A letter C/c/T/t followed by 4 letters/digits from 0-9 a-f A-F is read as a control code ("Gintaaaa", "Cabbed"):
  the check rejects it; stretch names at most to "Gintaaa".
- Item-get narration: "X / obtained!", "X / received!". 【】 -> [ ].
- Glossary decisions from wave 1 are at the end of `glossary.md`.

## Report (reply with only this)
Files written and entry count; then any lines: `NEW TERM: jp -> en`, `UNSURE: id - note`, `LONG: id - note`.
