# Fonts

Every font or glyph sheet the build reads ends up inside the released patch, so its licence must allow that. One row
per file; a font with no known licence doesn't go into a release.

| File | Source (URL, version) | Licence | Redistributable in a patch | Used for | Changes made |
|---|---|---|---|---|---|
| fonts/vwf8.txt | drawn for this project | MIT, same as repo | yes | dialogue/list VWF; small (8 px) sprite labels (`tools/gfxtext.py`) | - |
| fonts/PixelifySans.ttf | https://github.com/google/fonts/tree/main/ofl/pixelifysans (variable, 2021 Pixelify Sans Project Authors); licence `fonts/PixelifySans-OFL.txt` | OFL 1.1 | yes, as rendered glyphs | sprite labels at 13/11 px, Medium weight, no antialiasing (`tools/gfxtext.py`) | - |
