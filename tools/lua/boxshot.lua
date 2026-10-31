-- One screenshot per finished dialogue box: the MswStr window task reaches 0x080119CA when its last line is drawn
-- (docs/re/vwf.md). Shots are box_<frame>.png, taken 2 frames later so the last glyph is on screen.
local due = nil
L.on_exec(0x080119CA, 0x080119CA, function() due = L.frame + (BOXDELAY or 2) end) -- BOXDELAY: tour.py
L.on_frame(function(n)
  if due and n >= due then
    L.shot(string.format("box_%06d.png", n))
    due = nil
  end
end)
