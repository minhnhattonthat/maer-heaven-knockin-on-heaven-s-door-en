-- Log every distinct string the font renderers draw (docs/re/vwf.md): renderer, x/y where known, first bytes.
-- Use with warp.lua on the marker build: code strings show as [cN], records as [rN], script lines as [n].
--   emu.py build/marker.gba --out D --script tools/debug/warp.lua --script tools/lua/drawlog.lua --var "SCENE='x'"
-- Lines: "draw <renderer> <ptr> x=<x> y=<y> f<frame> <text>". Dialogue logs each line buffer copy (y = line).
local mem = emu.memType.gbaMemory
local seen = {}
local function text(p)
  local t = {}
  for i = 0, 47 do
    local c = emu.read(p + i, mem)
    if c == 0 then break end
    t[#t + 1] = (c >= 0x20 and c < 0x7F) and string.char(c) or string.format("\\x%02X", c)
  end
  return table.concat(t)
end
local function log(kind, p, x, y)
  local s = text(p)
  local k = kind .. s .. tostring(x) .. tostring(y)
  if seen[k] then return end
  seen[k] = true
  L.log(string.format("draw %s %08X x=%s y=%s f%d %s", kind, p, tostring(x), tostring(y), L.frame, s))
end
local function st() return emu.getState() end
-- dialogue window: strcpy(line buffer, src) per line, r1 = src
L.on_exec(0x0801182C, 0x0801182C, function() local s = st(); log("dlg", s["cpu.r1"], "-", "-") end)
-- centred label 0x0801E168(str, centre x, y)
L.on_exec(0x0801E168, 0x0801E168, function() local s = st(); log("ctr", s["cpu.r0"], s["cpu.r1"], s["cpu.r2"]) end)
-- list windows: at the x calculation, string = [[obj] + [sp+0x14]], byte index r8 (0 = first glyph)
local function list(kind, objreg)
  return function()
    local s = st()
    if s["cpu.r8"] ~= 0 then return end
    local obj = s["cpu." .. objreg]
    local arr = emu.read32(obj, mem, false)
    local i4 = emu.read32(s["cpu.r13"] + 0x14, mem, false)
    log(kind, emu.read32(arr + i4, mem, false), emu.read16(obj + 0x1C, mem, true), i4 // 4)
  end
end
L.on_exec(0x0805330C, 0x0805330C, list("list1", "r5"))
L.on_exec(0x0805345A, 0x0805345A, list("list2", "r4"))
