-- Log package/file lookups: exec of 0x0807AC3C (get file: r0 = package name, r1 = file name/index),
-- and the package slot table at [0x03006114] (24-byte slots, +0x10 = package base).
local mem = emu.memType.gbaMemory
local function str(p)
  if p < 0x02000000 or p > 0x09FFFFFF then return string.format("#%X", p) end
  local t = {}
  for i = 0, 40 do
    local c = emu.read(p + i, mem)
    if c == 0 then break end
    t[#t + 1] = string.char(c)
  end
  return table.concat(t)
end
local seen = {}
L.on_exec(0x0807AC3C, 0x0807AC3C, function()
  local s = emu.getState()
  local a, b = s["cpu.r0"], s["cpu.r1"]
  local key = str(a) .. "/" .. str(b)
  if seen[key] then return end
  seen[key] = true
  local tbl = emu.read32(0x03006114, mem, false)
  local base = emu.read32(tbl, mem, false)
  local n = emu.read32(tbl + 8, mem, false)
  local slots = {}
  for i = 0, math.min(n, 16) - 1 do
    local e = base + i * 24
    slots[#slots + 1] = string.format("%s@%08X", str(emu.read32(e + 8, mem, false)), emu.read32(e + 0x10, mem, false))
  end
  L.log(string.format("f%d get %s / %s lr=%08X  pkgs[%d] %s", L.frame, str(a), str(b), s["cpu.r14"], n,
    table.concat(slots, " ")))
end)
