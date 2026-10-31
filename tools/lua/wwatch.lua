-- Log distinct writers (PC) to WLO..WHI (--var WLO=0x... --var WHI=0x...) from frame WFROM on, with the first
-- address each wrote. Finds who overwrites a buffer (docs/re/vwf.md: script code copy vs. a fixed buffer).
local seen, n = {}, 0
L.on_write(WLO, WHI, function(addr, value)
  if L.frame < (WFROM or 0) then return end
  local pc = L.pc()
  if not seen[pc] and n < 60 then
    seen[pc] = true
    n = n + 1
    L.log(string.format("f%d write %08X by pc %08X", L.frame, addr, pc))
  end
end)
