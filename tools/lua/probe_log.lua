-- Setup check: proves --script hooks run and L.log reaches log.txt.
L.on_frame(function(n) if n == 60 then L.log("probe ok frame " .. n) end end)
