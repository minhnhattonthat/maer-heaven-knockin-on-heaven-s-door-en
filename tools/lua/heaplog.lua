-- Log every LZ77 script unpack (loader 0x080050A8 -> alloc at 0x080050C4: r0 = heap, r1 = size) with the heap's
-- block list: total size, free bytes and the largest free block, so the room scripts have can be measured
-- (docs/re/vwf.md). Block header: u32 size | flags (bit0 used, bit1 last), u32 prev?; blocks start at heap + 8.
local mem = emu.memType.gbaMemory
local function walk(heap)
  local p, total, free, big, n = heap + 8, 0, 0, 0, 0
  while n < 4000 do
    local h = emu.read32(p, mem, false)
    local size = h & ~3
    if size == 0 then break end
    total = total + size
    if h & 1 == 0 then
      free = free + size
      if size > big then big = size end
    end
    n = n + 1
    if h & 2 ~= 0 then break end
    p = p + size
  end
  return total, free, big, n
end
L.on_exec(0x080050C4, 0x080050C4, function()
  local s = emu.getState()
  local heap, size = s["cpu.r0"], s["cpu.r1"]
  local total, free, big, n = walk(heap)
  L.log(string.format("f%d unpack size %d heap %08X total %d free %d largest %d blocks %d", L.frame, size, heap,
    total, free, big, n))
end)
if ALLOCS then  -- --var ALLOCS=1: every alloc (0x0807A54C r0 heap, r1 size) with its caller and the heap state
  L.on_exec(0x0807A2EC, 0x0807A2EC, function()
    local s = emu.getState()
    L.log(string.format("f%d malloc(%d) from %08X", L.frame, s["cpu.r1"], s["cpu.r14"]))
  end)
  L.on_exec(0x0807A54C, 0x0807A54C, function()
    local s = emu.getState()
    local heap = s["cpu.r0"] ~= 0 and s["cpu.r0"] or emu.read32(0x03006110, mem, false)
    local total, free, big = walk(heap)
    L.log(string.format("f%d alloc %d heap %08X lr %08X free %d largest %d", L.frame, s["cpu.r1"], heap,
      s["cpu.r14"], free, big))
  end)
end
L.on_exec(0x080050C8, 0x080050C8, function()
  L.log(string.format("f%d -> %08X", L.frame, emu.getState()["cpu.r0"]))
end)
