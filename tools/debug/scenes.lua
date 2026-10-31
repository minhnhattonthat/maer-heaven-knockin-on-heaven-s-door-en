-- Scene list for tools/debug/warp.lua. Kinds (details in warp.lua):
--   chesc = offset of a "yes" block in CH_ESC.SPC, the game's own debug chapter select (`tools/debug/chesc.py`
--           lists them with the question text); the block sets party/flags itself and chains the event script;
--   npc   = script run in place of CH_ESC.SPC when the player talks to a debug-room NPC (shops, debug scripts);
--   script = script run in place of OPEN.SPC at new game;  boot = no warp.
-- route = inline route ("FRAMES BUTTONS;...") played once the warp is done (e.g. open a menu).
-- wait = frames after the warp before the proof shot / state (default 300); mash = press A every N frames meanwhile.
local S = {}
S.list = {
  -- boot / title
  copyright         = { boot = true, wait = 600, note = "copyright screen" },
  title             = { boot = true, wait = 900, note = "title screen (no warp)" },
  mode_select       = { boot = true, wait = 1450, route = "900 -;6 start;300 -;6 start", note = "title mode list" },
  mode_unlocked     = { boot = true, unlock = true, wait = 1450, route = "900 -;6 start;300 -;6 start",
                        note = "mode list with all modes lit" },
  mode_arm_trade    = { boot = true, unlock = true, wait = 1900, route = "900 -;6 start;300 -;6 start;200 -;6 down;40 -;6 a",
                        note = "ÄRM交換モード selected (A shows nothing new without a link partner)" },
  mode_versus       = { boot = true, unlock = true, wait = 1950,
                        route = "900 -;6 start;300 -;6 start;200 -;6 down;40 -;6 down;40 -;6 a", note = "対戦モード" },
  mode_dungeon      = { boot = true, unlock = true, wait = 2000,
                        route = "900 -;6 start;300 -;6 start;200 -;6 down;40 -;6 down;40 -;6 down;40 -;6 a",
                        note = "ダンジョンモード" },
  newgame           = { script = "OPEN.SPC", wait = 600, note = "normal new game: opening" },
  debug_room        = { npc = "CH_ESC.SPC", wait = 120, note = "debug room NPC menu (unpatched CH_ESC)" },
  -- story (CH_ESC questions, in order)
  opening           = { chesc = 0x01F2, note = "はじめからやる？ -> OPEN.SPC" },
  ev_start          = { chesc = 0x031A, note = "オープニングとばし -> EV_START.SPC" },
  altar             = { chesc = 0x0495, note = "祭壇の前 (MAP01_2A, going for Babbo)" },
  after_babbo       = { chesc = 0x0679, note = "バッボをゲットした後 (MAP00_A)" },
  jack_field        = { chesc = 0x096D, note = "オイラの畑の手前 (MAP40_A)" },
  garou_fight       = { chesc = 0x0B23, note = "ルーガルー戦の直前 -> EV_JA02" },
  garou_beaten      = { chesc = 0x0C74, note = "ルーガルーを倒した -> EV_JA04" },
  paz_town          = { chesc = 0x0E82, note = "パヅタウンの手前 (MAP41_A)" },
  babbo_thieves     = { chesc = 0x103D, note = "盗賊に奪われたバッボ -> EV_AL02" },
  ice_rescue        = { chesc = 0x1249, note = "あたしを助けに -> EV_ICE01" },
  ice_snow          = { chesc = 0x135A, note = "あたしの所まで来てる -> EV_ICE09" },
  ice_ian_beaten    = { chesc = 0x1467, note = "イアンも倒して -> EV_ICE11" },
  pelica            = { chesc = 0x1674, note = "ペリカに入った -> G_EV010" },
  gate_front        = { chesc = 0x177A, note = "修練の門の前 -> G_EV020" },
  gate_jack_dorothy = { chesc = 0x1892, note = "ジャックとドロシーが修練の門 -> EV_MON01" },
  gate_ginta_snow   = { chesc = 0x19A7, note = "ギンタとスノウが修練の門 -> G_EV021" },
  gate_done         = { chesc = 0x1AB3, note = "修練の門を終えた -> G_EV023" },
  ian_rematch       = { chesc = 0x1BC3, note = "イアンと再び -> EV_MON03" },
  jack_vs_gido      = { chesc = 0x1CCC, note = "ジャックとギド -> EV_MON04" },
  rubelia           = { chesc = 0x1EDB, note = "ルベリアの砦 -> G_EV002" },
  mar_status        = { chesc = 0x1FDF, note = "メルの現状 -> G_EV005" },
  magic_carpet      = { chesc = 0x2213, note = "マジックカーペット -> G_EV030" },
  vestry            = { chesc = 0x242D, note = "ヴェストリに入る -> EV_VE01" },
  vestry_lake       = { chesc = 0x2547, note = "ヴェストリから地底湖へ -> EV_GO01" },
  tom               = { chesc = 0x2655, note = "トムと行動 -> EV_GO06" },
  vestry_freed      = { chesc = 0x276D, note = "解放したヴェストリ -> EV_GO12" },
  three_dungeons    = { chesc = 0x297D, note = "３つのダンジョンの入り口 (MAP24_A)" },
  talos_hand        = { chesc = 0x2B10, note = "タロスの手 -> MAP24_4A" },
  talos_foot        = { chesc = 0x2C92, note = "タロスの足 -> MAP25_5A" },
  talos_head        = { chesc = 0x2E14, note = "タロスの頭 -> MAP26_2A" },
  talos             = { chesc = 0x2F92, note = "タロス (MAP26_5A)" },
  ending            = { chesc = 0x3222, note = "エンディング -> END2.SPC" },
  credits           = { chesc = 0x332D, mash = 40, mash_until = 600, wait = 1500, note = "スタッフロール -> SROLL.SPC" },
  credits_end       = { chesc = 0x332D, mash = 40, mash_until = 600, wait = 4600, note = "last credits page" },
  clear_password    = { chesc = 0x332D, mash = 40, mash_until = 600, wait = 5300, note = "CLEAR PASSWORD after the staff roll" },
  pelica_free       = { chesc = 0x3435, note = "イベント無しでペリカ (MAP42_A)" },
  rubelia_free      = { chesc = 0x3593, note = "イベント無しでルベリア (MAP06_A)" },
  -- debug helpers
  all_party         = { chesc = 0x3809, note = "全員使える (whole party, party change)" },
  full_items        = { chesc = 0x3E9D, note = "アイテムとＲＭを満タン -> FULL_ITM.SPC" },
  face_check        = { chesc = 0x4061, note = "フェイスチェック -> DBG_FACE.SPC (portraits)" },
  engraver          = { chesc = 0x4332, note = "彫金師ベリーニ (engraving menu)" },
  -- battle (Loup-Garou fight, mashing A through the intro and the fight)
  battle            = { chesc = 0x0B23, mash = 30, wait = 1000, note = "field battle vs Loup-Garou" },
  battle_arm_select = { chesc = 0x0B23, mash = 30, wait = 1440, note = "ARM SELECT screen in battle" },
  battle_win        = { chesc = 0x0B23, mash = 30, wait = 2200, note = "WIN screen" },
  game_over         = { chesc = 0x0B23, mash = 30, mash_until = 900, kill = 1150, wait = 1600, note = "leader HP set to 0" },
  -- field menu (START in the debug room)
  menu              = { chesc = 0x3435, wait = 600, route = "200 -;6 down;40 -;6 a;200 -;6 start",
                        note = "main menu (Pelica without event; answer the prompt no, then START)" },
  -- dungeon mode: S_DUNG.SPC at new game, gate chosen by forcing DungGetGenNo
  dungeon0          = { npc = "S_DUNG.SPC", gen = 0, wait = 100, note = "修練の門 BF1 banner" },
  dungeon1          = { npc = "S_DUNG.SPC", gen = 1, wait = 100, note = "gate 1 banner" },
  dungeon2          = { npc = "S_DUNG.SPC", gen = 2, wait = 100, note = "gate 2 banner" },
  dungeon3          = { npc = "S_DUNG.SPC", gen = 3, wait = 100, note = "練武の門 BF1 banner" },
  dungeon4          = { npc = "S_DUNG.SPC", gen = 4, wait = 100, note = "gate 4 banner" },
  -- NPC-context scripts (main-menu entries are added below the list)
  world_map         = { npc = "W_MAP.SPC", wait = 400, route = "60 -;6 up;40 -;6 a", note = "world map (answer yes)" },
  shop_a1          = { npc = "SHOPPA01.SPC", note = "ARM shop 1" },
  shop_a2           = { npc = "SHOPPA02.SPC" },
  shop_a3           = { npc = "SHOPPA03.SPC" },
  shop_a4           = { npc = "SHOPPA04.SPC" },
  shop_a5           = { npc = "SHOPPA05.SPC" },
  shop_e1           = { npc = "SHOPPE01.SPC" },
  shop_e2           = { npc = "SHOPPE02.SPC" },
}
-- main-menu entries (COMMAND list: deck edit, item, status, ARM list): the menu scene, then DOWN and A
local M = S.list.menu.route .. ";150 -"
S.list.menu_deck = { chesc = 0x3435, wait = 900, route = M .. ";6 a", note = "deck edit: pick a character" }
S.list.menu_deck_edit = { chesc = 0x3435, wait = 1100, route = M .. ";6 a;150 -;6 a", note = "deck edit screen" }
S.list.menu_item = { chesc = 0x3435, wait = 900, route = M .. ";6 down;30 -;6 a", note = "item list" }
S.list.menu_status = { chesc = 0x3435, wait = 900, route = M .. ";6 down;30 -;6 down;30 -;6 a", note = "status" }
S.list.menu_arm_list = { chesc = 0x3435, wait = 900, route = M .. ";6 down;30 -;6 down;30 -;6 down;30 -;6 a",
  note = "ARM list" }

-- Game state (docs/re/debug.md): G = [0x03003FDC]; story flags bit n at G+0xAC+(n>>3) (SetBool/GetBool),
-- vars u32 at G+0x2C+4n (SetVar/GetVar), play mode u16 at G+0x4258, party records G+0x35E0+0x54*i (HP s16 +2, max +4).
local mem = emu.memType.gbaMemory
local function G() return emu.read32(0x03003FDC, mem, false) end
function S.set_flag(n, on)
  local a = G() + 0xAC + (n >> 3)
  local b = emu.read(a, mem)
  emu.write(a, on and (b | (1 << (n & 7))) or (b & ~(1 << (n & 7))), mem)
end
function S.set_var(n, v) emu.write32(G() + 0x2C + 4 * n, v, mem) end
local peak = 0
function S.god() -- GOD=1: refill every party member's field HP each frame, and undo damage to the battle leader
  local g = G()
  if g < 0x02000000 then return end
  for i = 0, 7 do
    local r = g + 0x35E0 + 0x54 * i
    local mx = emu.read16(r + 4, mem, false)
    if mx > 0 and mx < 10000 then emu.write16(r + 2, mx, mem) end
  end
  local b = emu.read32(0x03004020, mem, false)
  if b < 0x02000000 or b >= 0x02040000 then return end
  local cur = emu.read16(b + 0x3A6, mem, false)
  if cur > peak and cur < 10000 then peak = cur
  elseif cur > 0 and cur < peak then S.btl_hp(peak) end
end
-- battle leader HP: 4 copies, all must change (u32 B+0x228 (setter 0x080096D8), B+0x22C (bar), B+0x604, u16 B+0x3A6)
-- with B = [0x03004020], unit stride 0x688; found by RAM search + write watch in the Loup-Garou fight
function S.btl_hp(v)
  local b = emu.read32(0x03004020, mem, false)
  if b >= 0x02000000 and b < 0x02040000 then
    emu.write32(b + 0x228, v, mem); emu.write32(b + 0x22C, v, mem); emu.write32(b + 0x604, v, mem)
    emu.write16(b + 0x3A6, v, mem)
  end
end
return S
