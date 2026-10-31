-- Cheats for a run that starts from a savestate (play.py sessions, emu.py --state-in), no warp:
--   play.py SESSION --rom ROM --state work/states/shop_a2.mss --script tools/debug/cheat.lua --var PEWTER=50000
-- Globals: PEWTER=n (money held at n every frame), GOD=1 (scenes.lua S.god), SCENES (path of scenes.lua).
local scenes = dofile(SCENES or "../debug/scenes.lua") -- Mesen's working folder is tools/mesen
L.on_frame(function()
  if PEWTER then scenes.set_pewter(PEWTER) end
  if GOD then scenes.god() end
end)
