-- Log every read of the first word of an LZ77/raw block in ROM range LO..HI (game cart addresses),
-- with the PC and r0-r3/lr, once per (pc, addr). Usage: --var LO=0x08560000 --var HI=0x08F30000
-- Prints the CPU register key names once, so other probes can use them.
-- Optional: --var "STARTS_FILE='C:/abs/starts.lua'" (defines STARTS={[addr]=true}) logs only those addresses.
local seen, named = {}, false
if STARTS_FILE then dofile(STARTS_FILE) end
L.on_read(LO, HI, function(addr, value)
  if STARTS and not STARTS[addr] then return end
  local s = emu.getState()
  if not named then
    local ks = {}
    for k, _ in pairs(s) do if k:find("^cpu%.") and not k:find("pipeline") then ks[#ks + 1] = k end end
    table.sort(ks); L.log("keys " .. table.concat(ks, " ")); named = true
  end
  local pc = L.pc()
  local key = string.format("%x:%x", pc, addr)
  if seen[key] then return end
  seen[key] = true
  local r = function(i) return s["cpu.r" .. i] or s["cpu.r[" .. i .. "]"] or -1 end
  L.log(string.format("f%d pc=%08X addr=%08X r0=%08X r1=%08X r2=%08X r3=%08X lr=%08X", L.frame, pc, addr,
    r(0), r(1), r(2), r(3), r(14)))
end)
