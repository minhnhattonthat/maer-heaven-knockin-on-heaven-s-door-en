# Graphics-text coverage (phase 8)

Every lettered row of `gfx/SYSTEM.tsv`, `gfx/EFFECT.tsv` and `gfx/BG.tsv`, and the cold-boot warp shot that shows it in
English (`tools/debug/regen.py build/maer_en.gba` -> `work/qa/scenes/<scene>.png`; tour shots `work/qa/tour/<scene>/`).
Build checked: 39e106f6 (2026-11-01). Previews of every row (original | English): `gfxtext.py preview`, `bgtext.py preview`.

| Group | Rows | Seen in | State |
|---|---|---|---|
| Title logo, copyright | BG T_TTL06, T_C01 | scenes/title, scenes/copyright | ok |
| Mode carousel | 1878-1888 | scenes/mode_select, mode_unlocked | ok |
| Dungeon Mode banner + bars | 1898-1906 | scenes/mode_dungeon (zoom work/qa/zoom/dbar.png) | ok |
| Story Mode banner + bars | 1889-1897 | scenes/mode_story (zoom work/qa/zoom/new2.png) | ok |
| Main menu | 0701-0705 | scenes/menu | ok |
| ÄRM type tags | 0537-0541 | scenes/battle_arm_select (AT, SPEC) | ok; DF/A+D/HEAL by preview only |
| ÄRM type balls | 0624-0635 | tour battle_arm_select (sheet_2) | ok |
| Power left, name tag on bar | 0054, 1820-1821 | scenes/menu_deck (zoom deckbar.png) | ok; other name tags (1822-1837) by preview only |
| Dungeon gate banners + BF | 0790-0794, 1574-1578 | scenes/dungeon0-4 | ok |
| Area names | 1561-1573 | - | **trigger not found**: no card on warp entry, debug-question entry or world-map arrival (Babbo's Ruins, shots every 15 frames); preview only |
| Shop windows / inn Yes-No | 1581, 1582, 1585, 1586 | scenes/shop_a1-a5, e1-e2 | ok |
| Item shop Owned, ÄRM shop OWNED | 0700, BG SP_BG12 | tour shop_a3 (zoom owned.png), scenes/shop_a1 | ok |
| Smith | BG SM_BG12, 1583, 1685 | scenes/engraver (list empty without materials) | 1583/1685 **not shot** (need materials) |
| Item command windows | 1508-1510, 1584, 1587-1590 | scenes/items_cmd (1510 Use/Drop) | 1510 ok; 1584/1587-1590 preview only (same window layout, same rects) |
| Input prompts | 1686-1687 | - | **not reachable from cold boot**: password entry is Dungeon Mode > Keep Exploring, greyed out without a save; recipe entry needs the smith with materials; preview only |
| Button hints | 1801-1815 | scenes/mode_versus, menu_deck, menu_arm_list, engraver | ok for those shown |
| Link-cable messages | 1816-1819 | - | unreachable without a link partner; preview only |
| Labels | 1782-1783, 1838-1841 | scenes/shop_*, mode_versus (Versus), work/qa/x_password/final.png (Dungeon) | Buy/Sell/Versus/Dungeon ok; 1782-1783 preview only |
| Staff roll | 1698-1781 | tour credits (zoom thanks.png, design.png) | ok |
| Game over | (already English) | scenes/game_over | ok |
| Sealed / Stats | EFFECT 0386-0389, 0402-0406 | - | **not shot yet** (battle effects) |
