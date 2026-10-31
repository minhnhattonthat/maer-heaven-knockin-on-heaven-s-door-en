# Graphics-text survey

Method (2026-11-01): static sweep of every graphic in MAR.NFP with `tools/gfxsweep.py work/gfx` (after
`tools/nfp.py extract work/nfp`): 192 KMP backgrounds rendered with their KCG tiles + KCL palette, 21 TCG/KCG tile
sets without a map, and all 9 252 sprite frames of the three NCD banks composed from their OAM entries (1 skipped:
`EFCSTART.KMP` names a KCG that doesn't exist, `TEST_M00.KCG`). Frames were deduplicated and packed into labelled
pages, read by five read-only visual-QA subagents; the smallest SYSTEM frames were re-read zoomed. Tour part: boot ->
logos -> copyright -> title -> mode carousel -> opening scene (`work/qa/smoke-orig`, `work/qa/mode*`). Mid-game
screens (dungeon banners, battle, credits, game over) are covered by the static sweep only until the phase 2 debug
tool can warp there; add any new find here.

Full per-frame lists: `gfx_survey/SYSTEM.tsv`, `BG.tsv`, `EFFECT_a.tsv`, `EFFECT_b.tsv`, `CHR.tsv` (page, frame or
image, text as read, what it is). `?` marks a doubtful reading; confirm against the screen when editing.

## NCD sprite format (verified: frames render as recognisable menus/labels)

`NCD (C)2004 NOBODY` header; +0x20 six u32 section offsets (names, anims, frames, OAM, palettes, tiles), +0x40 counts.
Names 16 B (name[8], u32 anim index, u32 count) -> anims 8 B (u32 frame index, u32 count) -> frames 8 B (u32 first
OAM, u16 count, u16 ?) -> OAM 20 B (u16 attr0, u16 attr1 as GBA OAM: y, shape, x, size, flips; u32 palette index;
u32 tile index; 8 B ?; the OAM y/x are the object's **centre**, not its top left: mixed-size frames such as shop
window 1585 only tile up that way, and objects relaid as top-left showed 8-16 px off in game) -> palettes 32 B each -> raw (uncompressed) 4bpp tiles, 1D mapping. Sprite tiles are not
compressed, so edits are in place if the new art uses no more tiles.

## Japanese in graphics (everything that needs work)

| Where | Items | Source | Notes |
|---|---|---|---|
| Title screen | メルヘヴン logo; katakana ノッキン オン ヘヴンズ ドア under the English subtitle | BG `T_TTL06` | D5: the series has an official English logo (MÄR), so the logo is in scope; the katakana line can simply be removed |
| Copyright screen | ©安西信行/小学館・ShoPro・TV Tokyo | BG `T_C01` | English: © Nobuyuki Anzai / Shogakukan ... |
| Mode select (title carousel) | ストーリーモード, ÄRM交換モード, 対戦モード, ダンジョンモード (lit/dim) + big animated banners; 2 faint strips 1893-1897, 1902-1906 | SYSTEM 1878-1906 | |
| Pause/main menu | デッキエディット, アイテム, ステータス, ÄRMリスト, パーティーへんせい, ゲットÄRM; しょす? label 0700 | SYSTEM 0700-0706 | |
| ARM type tags/icons | 攻, 防, 攻防, 回復, 特殊 | SYSTEM 0537-0541, 0624-0635 | single kanji in tiny cells: needs short English (ATK/DEF...) |
| Gauge label | 威力のこり | SYSTEM 0054 | |
| Dungeon gates | 修練/練磨/鍛錬/練武/最後の門 (+BF) | SYSTEM 0790-0794, 1574-1578 | |
| Area names | 遺跡, ジャックの家, 氷の城, パヅタウン?, ルベリアの岩?, ペリカの街(郊外), ヴェストリの村, ヴェストリ地底湖, オルターピース/アイス/ラヴァBF, ラストオルター | SYSTEM 1561-1573 | |
| Command windows | つかう/すてる, うる/かう/はい/はじめる/する/セーブ/しない (+ small second lines), ÄRMレシピ, smith menu アームシルバー/ゴールド/プラチナ + する/やめる | SYSTEM 1508-1510, 1581-1590, 1685; BG `SM_BG12` (+アームジュエル), `SP_BG12` (しょじすう) | |
| Input prompts | ÄRMレシピをいれてください, パスワードをいれてください | SYSTEM 1686-1687 | |
| Button hints | (A)けってい/デッキからはずす/デッキにいれる/せつめい/..., (B)やめる/おわる/もどる, (START)メニュー/デッキへんしゅう, (SELECT)ステータス/せつめい, (+)... | SYSTEM 1801-1815 | |
| Link-cable messages | つうしんをまっています..., つうしんにしっぱいしました..., つうしんエラーが発生しました | SYSTEM 1816-1819 | |
| Name tags | ギンタ, ジャック, スノウ, エドワード, アルヴィス, ナナシ, ドロシー, ファントム | SYSTEM 1820-1837 | |
| Shop/misc labels | かう, うる, ダンジョン, 通信対戦, キャラクターへんこう, ならびかえ | SYSTEM 1782-1783, 1838-1841 | |
| Staff credits | ~85 frames: logo, headings, staff names, コナミ株式会社 | SYSTEM 1698-1781 | D3: credits in English (names romanized) |
| Battle effects | 封印 (seal status), パラメータ (wipe-in banner) | EFFECT 0386-0389, 0402-0406 | |
| Intro art | chalk scribbles on a blackboard (unreadable) | BG `OP_07_A` | art; leave |

Already English (no work): EXIT, ÄRM SELECT, BATTLE!/WIN/LOSE/PAUSE/GAME OVER/DRAW, Level Up!/Miss!/Counter!/Cancel!,
CHARA/DUNGEON/AREA/PARTY SELECT, ÄRM DECK/LIST/SHOP/STOCK/TRADE/PREVIEW, ITEM SHOP, MAGICSTONE LIST, PASS WORD, SMITH,
STATUS, COMMAND, GET ÄRM, VERSUS MODE, PUSH START BUTTON, NEXT STOCK, CLEAR PASSWORD, CLASS/COST/RECIPE. Not text:
MÄR rune lettering (shop sign MAP10_A, magic circles DS_BG01/02, OP_09_A). CHR.NCD has no text.
