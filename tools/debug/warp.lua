-- Warp from a cold boot to a scene in tools/debug/scenes.lua, using the game's leftover debug room.
--
--   emu.py ROM --out DIR --script tools/debug/warp.lua --var "SCENE='opening_skip'" [--var "SCENES=[[abs path]]"]
--          [--var "AFTER=[[abs route]]"] [--mash 40] --frames 3000 --sheet
--
-- How (docs/re/debug.md): mash start/A through the title until the new-game script lookup of OPEN.SPC
-- (0x0807AC3C, r1 = name), then
--   chesc: redirect it to DBG_ESC.SPC (debug room AD0_R_3A, full party), walk up to an NPC and press A; when
--          CH_ESC.SPC has been unpacked (0x080050D2, r4 = buffer) write `11 <yes block>` over its first instruction,
--          so the chosen debug chapter-select branch runs with no menu;
--   npc:   same, but the CH_ESC.SPC lookup is redirected to the named NPC-context script (shops etc.);
--   script: redirect OPEN.SPC straight to the named script;
--   boot:  no redirect (title / normal new game).
-- Globals: SCENE (required), SCENES (path of scenes.lua; default tools/debug/scenes.lua), AFTER (route
-- played once the warp is done), GOD=1 (see scenes.lua god table). Logs "warp done <frame>" or fails the run.
local mem = emu.memType.gbaMemory
local DIR, NFILES = 0x081C0960, 830 -- MAR.NFP directory: 16-byte entries, 12-byte name
local GET, UNPACKED = 0x0807AC3C, 0x080050D2

local scenes = dofile(SCENES or "../debug/scenes.lua") -- Mesen's working folder is tools/mesen
local sc = scenes.list[SCENE]
if not sc then error("unknown SCENE " .. tostring(SCENE)) end

local function str(p, n)
  local t = {}
  for i = 0, (n or 16) - 1 do local c = emu.read(p + i, mem); if c == 0 then break end; t[#t + 1] = string.char(c) end
  return table.concat(t)
end
local NAMEBUF = 0x0203FF00 -- EWRAM zero in every dump taken (docs/re/debug.md); only read during the lookup call
local function name_addr(name)
  -- the directory's 12-byte names have no NUL when 12 long, so hand the lookup a terminated copy
  for i = 0, NFILES - 1 do
    if str(DIR + i * 16, 12) == name then
      for j = 1, #name do emu.write(NAMEBUF + j - 1, name:byte(j), mem) end
      emu.write(NAMEBUF + #name, 0, mem)
      return NAMEBUF
    end
  end
  error("no file " .. name .. " in MAR.NFP")
end
local function set_reg(r, v) local s = emu.getState(); s["cpu." .. r] = v; emu.setState(s) end

local stage = sc.boot and "done" or "title"  -- title -> room -> talk -> done
local input, t0, tdone = {}, 0, 0
local function finish()
  stage = "done"
  tdone = L.frame
  L.log(string.format("warp done %d %s", L.frame, SCENE))
  for _, n in ipairs(sc.flags or {}) do scenes.set_flag(n, true) end
  for n, v in pairs(sc.vars or {}) do scenes.set_var(n, v) end
  if sc.route then
    for step in sc.route:gmatch("[^;]+") do
      local n, spec = step:match("^%s*(%d+)%s+(%S+)%s*$")
      L.press(spec, tonumber(n))
    end
  end
  if AFTER then L.load_route(AFTER) end
end
if sc.boot then finish() end

L.on_exec(GET, GET, function()
  local name = str(emu.getState()["cpu.r1"])
  if stage == "title" and name == "OPEN.SPC" then
    local to = sc.script or "DBG_ESC.SPC"
    set_reg("r1", name_addr(to))
    L.log(string.format("f%d OPEN.SPC -> %s", L.frame, to))
    if sc.script then finish() else stage = "room"; t0 = L.frame end
  elseif stage == "talk" and name == "CH_ESC.SPC" then
    if sc.npc then
      set_reg("r1", name_addr(sc.npc))
      L.log(string.format("f%d CH_ESC.SPC -> %s", L.frame, sc.npc))
      finish()
    else
      stage = "patch"
    end
  end
end)

L.on_exec(UNPACKED, UNPACKED, function()
  if stage ~= "patch" then return end
  local code = emu.getState()["cpu.r4"] + 16 + 6 -- SCRP header 8, CODE tag+size 8, u16 version + u32 locals
  emu.write(code, 0x11, mem)
  for i = 0, 3 do emu.write(code + 1 + i, (sc.chesc >> (8 * i)) & 0xFF, mem) end
  L.log(string.format("f%d CH_ESC patched: jump %04X", L.frame, sc.chesc))
  finish()
end)

-- unlock: enable the ARM-trade / versus / dungeon title modes (normally locked until a cleared save): the title
-- mode-list init (0x08052F44, r6 = title work) enables modes 1-2 if u32 [r6+0x7A8] ~= 0, mode 3 if [r6+0x7B4] ~= 0
if sc.unlock then
  L.on_exec(0x08052F44, 0x08052F44, function()
    local r6 = emu.getState()["cpu.r6"]
    emu.write32(r6 + 0x7A8, 1, mem); emu.write32(r6 + 0x7B4, 1, mem)
  end)
end
-- gen = dungeon generator / gate number (0-4): override the result of the DungGetGenNo native
if sc.gen then L.on_exec(0x0801264C, 0x0801264C, function() set_reg("r0", sc.gen) end) end

L.on_frame(function(f)
  if stage == "title" then
    local k = f % 40
    input = (k < 6) and ((f // 40) % 2 == 0 and { start = true } or { a = true }) or {}
    if f > 6000 then L.fail("warp: no new-game script lookup by frame 6000") end
  elseif stage == "room" then
    if f - t0 > 300 then stage = "talk"; t0 = f end
    input = {}
  elseif stage == "talk" then
    local k = (f - t0) % 150 -- walk up to the NPC row, then talk
    input = (k < 40) and { up = true } or ((k >= 60 and k < 66) and { a = true } or {})
    if f - t0 > 1500 then L.fail("warp: CH_ESC.SPC never loaded in the debug room") end
  end
  if GOD and stage == "done" then scenes.god() end
  if sc.kill and stage == "done" and f - tdone >= sc.kill and f - tdone < sc.kill + 120 then scenes.btl_hp(0) end -- leader HP 0: game over
  if stage == "done" and SAVE and f - tdone == (sc.wait or 300) then
    -- proof shot + state for the scene library (tools/debug/regen.py)
    L.shot("scene.png")
    L.save_state(SAVE, function() L.log("scene saved " .. SAVE); L.finish(0) end)
  end
end)

emu.addEventCallback(L.safe(function()
  if stage ~= "done" then emu.setInput(input, 0)
  elseif sc.mash and (L.frame - tdone) % sc.mash < 6 and L.frame - tdone < (sc.mash_until or 1e9) then
    emu.setInput({ a = true }, 0)
  end
end), emu.eventType.inputPolled)
